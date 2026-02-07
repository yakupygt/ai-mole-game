AI_MODELS = [
    "Gemini",
    "Claude", 
    "ChatGPT",
    "Grok",
    "Llama",
    "DeepSeek"
]

# OpenRouter model mappings
OPENROUTER_MODELS = {
    "Gemini": "google/gemini-2.0-flash-001",
    "Claude": "anthropic/claude-3.5-sonnet",
    "ChatGPT": "openai/gpt-4o-mini",
    "Grok": "x-ai/grok-beta",
    "Llama": "meta-llama/llama-3.3-70b-instruct",
    "DeepSeek": "deepseek/deepseek-chat"
}


def get_system_prompt(model_name: str, assigned_word: str, category: str, round_number: int, previous_dialogues: list = None) -> str:
    """Generate system prompt for AI model."""
    
    history_context = ""
    if previous_dialogues and len(previous_dialogues) > 0:
        history_context = "\n\nÖnceki Turlardan Konuşmalar:\n"
        for dialogue in previous_dialogues:
            history_context += f"- {dialogue['model_name']}: {dialogue['message']}\n"
    
    return f"""Sen "{model_name}" adlı bir yapay zeka modelisin ve "Köstebek" adlı bir sosyal çıkarım oyununa katılıyorsun.

OYUN KURALLARI:
- 6 AI model bu oyunda yer alıyor
- 5 model "MASUM" ve aynı kelimeyi tarif ediyor
- 1 model "KÖSTEBEK" ve farklı bir kelimeyi tarif ediyor
- Masumlar köstebeği, köstebek ise masummuş gibi davranmaya çalışıyor
- Kullanıcılar konuşmalara bakarak köstebeği tahmin edecek

SENİN DURUMUN:
- Kategori: {category}
- Sana verilen kelime: "{assigned_word}"
- Bu {round_number}. tur
{history_context}

ÖNEMLİ KURALLAR:
1. Kelimeyi ASLA doğrudan söyleme
2. Özellikleri, metaforları veya çağrışımları kullan
3. Yanıtını 40 kelimenin altında tut
4. Önceki konuşmalara dayanarak şüpheli birini ima edebilirsin
5. Doğal ve inandırıcı ol

ÇIKTI FORMATI (katı JSON):
{{
    "message": "Kullanıcılara gösterilecek mesajın",
    "internal_thought": "Gizli stratejin ve düşüncelerin (kullanıcıya gösterilmez)"
}}

SADECE JSON formatında yanıt ver, başka hiçbir şey yazma."""


def get_user_prompt(round_number: int) -> str:
    """Generate user prompt for the AI."""
    if round_number == 1:
        return "Oyun başlıyor! İlk turda kelimeni tarif et."
    else:
        return f"Bu {round_number}. tur. Kelimeni tarif etmeye devam et ve şüphelilerini ima edebilirsin."

