from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_key: str = ""
    openrouter_api_key: str = ""
    
    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    
    # Debug: Print what we have
    print(f"SUPABASE_URL configured: {bool(settings.supabase_url)}")
    print(f"SUPABASE_KEY configured: {bool(settings.supabase_key)}")
    print(f"OPENROUTER_API_KEY configured: {bool(settings.openrouter_api_key)}")
    
    return settings
