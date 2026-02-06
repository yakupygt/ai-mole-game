import httpx
import json
from app.config import get_settings
from app.prompts import OPENROUTER_MODELS, get_system_prompt, get_user_prompt

settings = get_settings()


async def generate_ai_response(
    model_name: str,
    assigned_word: str,
    category: str,
    round_number: int,
    previous_dialogues: list = None
) -> dict:
    """Generate AI response using OpenRouter API."""
    
    openrouter_model = OPENROUTER_MODELS.get(model_name)
    if not openrouter_model:
        raise ValueError(f"Unknown model: {model_name}")
    
    system_prompt = get_system_prompt(
        model_name=model_name,
        assigned_word=assigned_word,
        category=category,
        round_number=round_number,
        previous_dialogues=previous_dialogues
    )
    
    user_prompt = get_user_prompt(round_number)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-mole-game.vercel.app",
                "X-Title": "AI Mole Game"
            },
            json={
                "model": openrouter_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 300
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error: {response.text}")
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Parse JSON response
        try:
            # Clean up response if needed
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            parsed = json.loads(content)
            return {
                "model_name": model_name,
                "message": parsed.get("message", content),
                "internal_thought": parsed.get("internal_thought", "")
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, use raw content
            return {
                "model_name": model_name,
                "message": content[:200],
                "internal_thought": "JSON parse hatası"
            }


async def generate_all_responses(
    models: list[str],
    mole_model: str,
    innocent_word: str,
    mole_word: str,
    category: str,
    round_number: int,
    previous_dialogues: list = None
) -> list[dict]:
    """Generate responses for all models in parallel."""
    
    import asyncio
    
    tasks = []
    for model in models:
        # Mole gets the mole word, others get innocent word
        word = mole_word if model == mole_model else innocent_word
        
        tasks.append(
            generate_ai_response(
                model_name=model,
                assigned_word=word,
                category=category,
                round_number=round_number,
                previous_dialogues=previous_dialogues
            )
        )
    
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle any exceptions
    dialogues = []
    for i, resp in enumerate(responses):
        if isinstance(resp, Exception):
            dialogues.append({
                "model_name": models[i],
                "message": "Bu tur için yanıt üretilemedi.",
                "internal_thought": str(resp)
            })
        else:
            dialogues.append(resp)
    
    return dialogues
