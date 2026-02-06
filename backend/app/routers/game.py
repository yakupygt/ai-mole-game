from fastapi import APIRouter, HTTPException
from datetime import date
from app.models import PlayTurnRequest, PlayTurnResponse, DailyInfoResponse, ModelDialogue
from app.services.game_engine import get_today_setup, create_daily_setup
from app.services.cache_service import compute_state_hash, get_cached_state, save_game_state
from app.services.ai_service import generate_all_responses

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/daily", response_model=DailyInfoResponse)
async def get_daily_info():
    """Get today's game setup and first round."""
    
    setup = get_today_setup()
    
    if not setup:
        # Create setup if it doesn't exist (for testing)
        setup = await create_daily_setup()
        setup = get_today_setup()
    
    if not setup:
        raise HTTPException(status_code=404, detail="Today's game not available")
    
    # Get initial state from cache
    today = date.today()
    initial_hash = compute_state_hash(today, 1, setup["turn_order"], "START")
    cached = get_cached_state(initial_hash)
    
    if not cached:
        raise HTTPException(status_code=500, detail="Initial game state not generated")
    
    dialogues = [ModelDialogue(**d) for d in cached["dialogues"]]
    
    return DailyInfoResponse(
        date=setup["date"],
        category=setup["category"],
        turn_order=setup["turn_order"],
        initial_state_hash=initial_hash,
        round_number=1,
        dialogues=dialogues
    )


@router.post("/play_turn", response_model=PlayTurnResponse)
async def play_turn(request: PlayTurnRequest):
    """Play a turn - PASS or ELIMINATE a model."""
    
    setup = get_today_setup()
    if not setup:
        raise HTTPException(status_code=404, detail="Today's game not available")
    
    today = date.today()
    
    # Get current state
    if request.current_state_hash:
        current_state = get_cached_state(request.current_state_hash)
        if not current_state:
            raise HTTPException(status_code=400, detail="Invalid state hash")
        
        current_round = current_state["round_number"]
        remaining_models = current_state["remaining_models"]
    else:
        # Starting from round 1
        current_round = 1
        remaining_models = setup["turn_order"]
    
    # Validate action
    if request.action == "PASS":
        # Pass only allowed in round 1
        if current_round != 1:
            raise HTTPException(status_code=400, detail="PASS only allowed in round 1")
        
        new_round = 2
        new_remaining = remaining_models
        eliminated = None
        
    elif request.action == "ELIMINATE":
        if not request.target_model:
            raise HTTPException(status_code=400, detail="target_model required for ELIMINATE")
        
        if request.target_model not in remaining_models:
            raise HTTPException(status_code=400, detail="Invalid target model")
        
        new_remaining = [m for m in remaining_models if m != request.target_model]
        eliminated = request.target_model
        new_round = current_round + 1
        
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    # Check game over conditions
    game_over = False
    winner = None
    
    if request.action == "ELIMINATE":
        if request.target_model == setup["mole_model"]:
            # Found the mole - user wins!
            game_over = True
            winner = "USER"
        elif len(new_remaining) <= 2:
            # Mole survived - mole wins!
            game_over = True
            winner = "MOLE"
    
    # Compute new state hash
    new_hash = compute_state_hash(today, new_round, new_remaining, request.action, eliminated)
    
    # Check cache
    cached = get_cached_state(new_hash)
    
    if cached:
        # Return cached response
        dialogues = [ModelDialogue(**d) for d in cached["dialogues"]]
        return PlayTurnResponse(
            state_hash=new_hash,
            round_number=new_round,
            remaining_models=new_remaining,
            dialogues=dialogues,
            game_over=cached["game_over"],
            winner=cached.get("winner"),
            can_pass=False,
            eliminated_model=eliminated
        )
    
    # Generate new dialogues if game not over
    if game_over:
        dialogues_data = []
    else:
        # Get previous dialogues for context
        previous_dialogues = []
        if request.current_state_hash:
            prev_state = get_cached_state(request.current_state_hash)
            if prev_state:
                previous_dialogues = prev_state["dialogues"]
        
        dialogues_data = await generate_all_responses(
            models=new_remaining,
            mole_model=setup["mole_model"],
            innocent_word=setup["innocent_word"],
            mole_word=setup["mole_word"],
            category=setup["category"],
            round_number=new_round,
            previous_dialogues=previous_dialogues
        )
    
    # Save to cache
    save_game_state(
        state_hash=new_hash,
        game_date=today,
        round_number=new_round,
        remaining_models=new_remaining,
        action=request.action,
        dialogues=dialogues_data,
        game_over=game_over,
        winner=winner,
        eliminated_model=eliminated
    )
    
    dialogues = [ModelDialogue(**d) for d in dialogues_data]
    
    return PlayTurnResponse(
        state_hash=new_hash,
        round_number=new_round,
        remaining_models=new_remaining,
        dialogues=dialogues,
        game_over=game_over,
        winner=winner,
        can_pass=False,
        eliminated_model=eliminated
    )


@router.post("/cron/daily-setup")
async def trigger_daily_setup(secret: str = None):
    """Trigger daily setup - called by cron job."""
    
    # In production, validate secret key
    try:
        setup = await create_daily_setup()
        return {"status": "success", "date": setup["date"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
