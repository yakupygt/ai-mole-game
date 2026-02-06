from pydantic import BaseModel
from typing import Optional
from datetime import date


class WordPair(BaseModel):
    id: str
    category: str
    innocent_word: str
    mole_word: str
    difficulty: int = 3


class DailySetup(BaseModel):
    id: str
    date: date
    word_pair_id: str
    mole_model: str
    turn_order: list[str]
    innocent_word: Optional[str] = None
    mole_word: Optional[str] = None


class ModelDialogue(BaseModel):
    model_name: str
    message: str
    internal_thought: Optional[str] = None


class GameState(BaseModel):
    id: str
    state_hash: str
    date: date
    round_number: int
    remaining_models: list[str]
    action: str
    eliminated_model: Optional[str] = None
    dialogues: list[ModelDialogue]
    game_over: bool = False
    winner: Optional[str] = None


class PlayTurnRequest(BaseModel):
    action: str  # "PASS" or "ELIMINATE"
    target_model: Optional[str] = None
    current_state_hash: Optional[str] = None


class PlayTurnResponse(BaseModel):
    state_hash: str
    round_number: int
    remaining_models: list[str]
    dialogues: list[ModelDialogue]
    game_over: bool
    winner: Optional[str] = None
    can_pass: bool
    eliminated_model: Optional[str] = None


class DailyInfoResponse(BaseModel):
    date: str
    category: str
    turn_order: list[str]
    initial_state_hash: str
    round_number: int
    dialogues: list[ModelDialogue]
