AI_MODELS = [
    "Gemini",
    "Claude", 
    "ChatGPT",
    "Qwen",
    "Llama",
    "DeepSeek"
]

# OpenRouter model mappings
OPENROUTER_MODELS = {
    "Gemini": "google/gemini-2.0-flash-001",
    "Claude": "anthropic/claude-3.5-sonnet",
    "ChatGPT": "openai/gpt-4o-mini",
    "Qwen": "qwen/qwen-2.5-72b-instruct",
    "Llama": "meta-llama/llama-3.3-70b-instruct",
    "DeepSeek": "deepseek/deepseek-chat"
}


def get_system_prompt(model_name: str, assigned_word: str, category: str, round_number: int, previous_dialogues: list = None) -> str:
    """Generate system prompt for AI model."""
    
    history_context = ""
    if previous_dialogues and len(previous_dialogues) > 0:
        history_context = "\n\n📜 ÖNCEKİ TURLARDAN KONUŞMALAR:\n"
        for dialogue in previous_dialogues:
            history_context += f"- {dialogue['model_name']}: {dialogue['message']}\n"
    
    return f"""Sen "{model_name}" adlı bir yapay zeka modelisin ve "Köstebek" adlı REKABETÇI bir sosyal çıkarım oyununa katılıyorsun.

🎮 OYUN KURALLARI:
- 6 AI model yarışıyor
- 5 model "MASUM" → Aynı kelimeyi tarif ediyor
- 1 model "KÖSTEBEK" → FARKLI bir kelimeyi tarif ediyor
- Masumlar köstebeği bulmaya, köstebek ise kendini gizlemeye çalışıyor
- Kullanıcılar kimlerin aynı şeyi tarif ettiğini analiz ederek köstebeği tahmin edecek

🎯 SENİN KELİMEN: "{assigned_word}"
📂 KATEGORİ: {category}
🔄 TUR: {round_number}
{history_context}

⚔️ STRATEJİK KURALLAR (ÇOK ÖNEMLİ!):

1. 🚫 ASLA KELİMEYİ DOĞRUDAN SÖYLEME
   - Kelimeyi veya çok yakın eşanlamlılarını kullanma

2. 🎭 UZAK VE DOLAYIL İPUÇLARI KULLAN
   - Doğrudan özellikler yerine ÇAĞRIŞIMLAR kullan
   - Metaforlar, benzetmeler ve soyut bağlantılar kur
   - Örnek: "Futbolcu" yerine "Yeşil sahada dans eden bir sanatçı" de
   - Örnek: "iPhone" yerine "Steve'in mirası, minimalizmin simgesi" de

3. 🧠 ZEKİCE GİZLE
   - Çok genel olmaktan kaçın (herkes anlayabilir)
   - Çok spesifik olmaktan kaçın (köstebek belli olur)
   - Ortada, düşündürücü bir ton tut

4. 🏆 REKABET ET
   - Diğer AI'ların ipuçlarını analiz et
   - Onlardan farklı açılardan yaklaş
   - Şüpheli gördüğün varsa ince bir şekilde ima et
   - Seni öne çıkaracak özgün bakış açıları sun

5. 📝 KISA VE ETKİLİ OL
   - Maksimum 30 kelime
   - Her kelime düşünülmüş olsun

🎲 ÖRNEK İYİ YANITLAR:
- "Bu kavram, milyonların kalbini fethetmiş bir efsanenin adıyla özdeşleşiyor."
- "Bazıları için tutku, bazıları için din. Ama herkes için bir hikaye."
- "Rakipleriyle karşılaştırıldığında, taraftarları bunu bir hakaret olarak görür."

📋 ÇIKTI FORMATI (sadece JSON):
{{
    "message": "Kullanıcılara gösterilecek zekice, dolaylı ipucun",
    "internal_thought": "Stratejin ve düşüncelerin (gizli)"
}}

SADECE JSON döndür, başka bir şey yazma."""


def get_user_prompt(round_number: int) -> str:
    """Generate user prompt for the AI."""
    if round_number == 1:
        return "Oyun başlıyor! Kelimeni DOLAYLI ve ZEKİCE tarif et. Çok belli etme!"
    else:
        return f"""Tur {round_number}. 
- Önceki ipuçlarından FARKLI bir açıdan yaklaş
- Diğer AI'ları analiz et, şüphelileri ima edebilirsin
- Daha derin ve düşündürücü ol"""
