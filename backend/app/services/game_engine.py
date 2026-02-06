import random
from datetime import date, datetime
from app.database import get_db
from app.prompts import AI_MODELS
from app.services.cache_service import compute_state_hash, save_game_state
from app.services.ai_service import generate_all_responses


def get_random_word_pair() -> dict:
    """Get a random word pair from database."""
    
    db = get_db()
    
    # Get all word pairs and select random
    result = db.table("word_pairs").select("*").execute()
    
    if not result.data:
        raise Exception("No word pairs found in database")
    
    return random.choice(result.data)


def select_random_mole() -> str:
    """Select a random model to be the mole."""
    return random.choice(AI_MODELS)


def generate_turn_order() -> list[str]:
    """Generate random turn order for models."""
    models = AI_MODELS.copy()
    random.shuffle(models)
    return models


async def create_daily_setup() -> dict:
    """Create daily setup - called by cron job at midnight."""
    
    db = get_db()
    today = date.today()
    
    # Check if setup already exists
    existing = db.table("daily_setup").select("*").eq("date", today.isoformat()).execute()
    if existing.data and len(existing.data) > 0:
        return existing.data[0]
    
    # Get random word pair
    word_pair = get_random_word_pair()
    
    # Select random mole and turn order
    mole_model = select_random_mole()
    turn_order = generate_turn_order()
    
    # Create daily setup
    setup_data = {
        "date": today.isoformat(),
        "word_pair_id": word_pair["id"],
        "mole_model": mole_model,
        "turn_order": turn_order
    }
    
    result = db.table("daily_setup").insert(setup_data).execute()
    setup = result.data[0]
    
    # Generate first round immediately
    await generate_first_round(setup, word_pair)
    
    return setup


async def generate_first_round(setup: dict, word_pair: dict):
    """Generate first round dialogues and cache them."""
    
    today = date.today()
    round_number = 1
    remaining_models = setup["turn_order"]
    action = "START"
    
    # Compute hash for initial state
    state_hash = compute_state_hash(today, round_number, remaining_models, action)
    
    # Generate dialogues
    dialogues = await generate_all_responses(
        models=remaining_models,
        mole_model=setup["mole_model"],
        innocent_word=word_pair["innocent_word"],
        mole_word=word_pair["mole_word"],
        category=word_pair["category"],
        round_number=round_number
    )
    
    # Save to cache
    save_game_state(
        state_hash=state_hash,
        game_date=today,
        round_number=round_number,
        remaining_models=remaining_models,
        action=action,
        dialogues=dialogues
    )


def get_today_setup() -> dict:
    """Get today's game setup."""
    
    db = get_db()
    today = date.today()
    
    result = db.table("daily_setup").select("*, word_pairs(*)").eq("date", today.isoformat()).execute()
    
    if not result.data:
        return None
    
    setup = result.data[0]
    word_pair = setup.get("word_pairs", {})
    
    return {
        "id": setup["id"],
        "date": setup["date"],
        "word_pair_id": setup["word_pair_id"],
        "mole_model": setup["mole_model"],
        "turn_order": setup["turn_order"],
        "category": word_pair.get("category", ""),
        "innocent_word": word_pair.get("innocent_word", ""),
        "mole_word": word_pair.get("mole_word", "")
    }
