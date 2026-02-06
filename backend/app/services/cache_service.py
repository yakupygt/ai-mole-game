import hashlib
from datetime import date
from app.database import get_db


def compute_state_hash(
    game_date: date,
    round_number: int,
    remaining_models: list[str],
    action: str,
    eliminated_model: str = None
) -> str:
    """Compute MD5 hash for game state."""
    
    # Sort models for consistent hashing
    sorted_models = sorted(remaining_models)
    
    hash_input = f"{game_date.isoformat()}|{round_number}|{','.join(sorted_models)}|{action}|{eliminated_model or ''}"
    
    return hashlib.md5(hash_input.encode()).hexdigest()


def get_cached_state(state_hash: str) -> dict | None:
    """Get cached game state from Supabase."""
    
    db = get_db()
    
    result = db.table("game_states").select("*").eq("state_hash", state_hash).execute()
    
    if result.data and len(result.data) > 0:
        return result.data[0]
    
    return None


def save_game_state(
    state_hash: str,
    game_date: date,
    round_number: int,
    remaining_models: list[str],
    action: str,
    dialogues: list[dict],
    game_over: bool = False,
    winner: str = None,
    eliminated_model: str = None
) -> dict:
    """Save game state to Supabase."""
    
    db = get_db()
    
    data = {
        "state_hash": state_hash,
        "date": game_date.isoformat(),
        "round_number": round_number,
        "remaining_models": remaining_models,
        "action": action,
        "eliminated_model": eliminated_model,
        "dialogues": dialogues,
        "game_over": game_over,
        "winner": winner
    }
    
    result = db.table("game_states").insert(data).execute()
    
    return result.data[0] if result.data else data
