from fastapi import APIRouter, HTTPException
from datetime import date
import traceback
from app.models import PlayTurnRequest, PlayTurnResponse, DailyInfoResponse, ModelDialogue
from app.services.game_engine import get_today_setup, create_daily_setup
from app.services.cache_service import compute_state_hash, get_cached_state, save_game_state
from app.services.ai_service import generate_all_responses

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/daily")
async def get_daily_info():
    """Get today's game setup and first round."""
    
    try:
        setup = get_today_setup()
        
        if not setup:
            # Create setup if it doesn't exist
            print("Creating new daily setup...")
            await create_daily_setup()
            setup = get_today_setup()
        
        if not setup:
            raise HTTPException(status_code=500, detail="Could not create daily setup")
        
        # Get initial state from cache
        today = date.today()
        initial_hash = compute_state_hash(today, 1, setup["turn_order"], "START")
        cached = get_cached_state(initial_hash)
        
        # If no cached dialogues, generate them now
        if not cached or not cached.get("dialogues"):
            print("Generating first round dialogues...")
            
            dialogues_data = await generate_all_responses(
                models=setup["turn_order"],
                mole_model=setup["mole_model"],
                innocent_word=setup["innocent_word"],
                mole_word=setup["mole_word"],
                category=setup["category"],
                round_number=1
            )
            
            # Save to cache
            save_game_state(
                state_hash=initial_hash,
                game_date=today,
                round_number=1,
                remaining_models=setup["turn_order"],
                action="START",
                dialogues=dialogues_data
            )
            
            cached = get_cached_state(initial_hash)
        
        dialogues = [ModelDialogue(**d) for d in cached["dialogues"]] if cached else []
        
        return {
            "date": setup["date"],
            "category": setup.get("category", "Bilinmiyor"),
            "turn_order": setup["turn_order"],
            "initial_state_hash": initial_hash,
            "round_number": 1,
            "dialogues": [{"model_name": d.model_name, "message": d.message} for d in dialogues]
        }
        
    except Exception as e:
        print(f"Error in get_daily_info: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/play_turn")
async def play_turn(request: PlayTurnRequest):
    """Play a turn - PASS or ELIMINATE a model."""
    
    try:
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
            if current_round != 1:
                raise HTTPException(status_code=400, detail="PASS only allowed in round 1")
            
            new_round = 2
            new_remaining = remaining_models
            eliminated = None
            
        elif request.action == "ELIMINATE":
            if not request.target_model:
                raise HTTPException(status_code=400, detail="target_model required")
            
            if request.target_model not in remaining_models:
                raise HTTPException(status_code=400, detail="Invalid target model")
            
            new_remaining = [m for m in remaining_models if m != request.target_model]
            eliminated = request.target_model
            new_round = current_round + 1
            
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Check game over
        game_over = False
        winner = None
        
        if request.action == "ELIMINATE":
            if request.target_model == setup["mole_model"]:
                game_over = True
                winner = "USER"
            elif len(new_remaining) <= 2:
                game_over = True
                winner = "MOLE"
        
        # Compute new state hash
        new_hash = compute_state_hash(today, new_round, new_remaining, request.action, eliminated)
        
        # Check cache
        cached = get_cached_state(new_hash)
        
        if cached:
            dialogues = [{"model_name": d["model_name"], "message": d["message"]} for d in cached["dialogues"]]
            return {
                "state_hash": new_hash,
                "round_number": new_round,
                "remaining_models": new_remaining,
                "dialogues": dialogues,
                "game_over": cached["game_over"],
                "winner": cached.get("winner"),
                "can_pass": False,
                "eliminated_model": eliminated
            }
        
        # Generate new dialogues if game not over
        if game_over:
            dialogues_data = []
        else:
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
        
        dialogues = [{"model_name": d["model_name"], "message": d["message"]} for d in dialogues_data]
        
        return {
            "state_hash": new_hash,
            "round_number": new_round,
            "remaining_models": new_remaining,
            "dialogues": dialogues,
            "game_over": game_over,
            "winner": winner,
            "can_pass": False,
            "eliminated_model": eliminated
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in play_turn: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    from app.config import get_settings
    
    try:
        settings = get_settings()
        return {
            "status": "healthy",
            "supabase_configured": bool(settings.supabase_url and "supabase" in settings.supabase_url),
            "openrouter_configured": bool(settings.openrouter_api_key and len(settings.openrouter_api_key) > 10)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
