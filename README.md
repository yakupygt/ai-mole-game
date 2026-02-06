# AI Köstebek Oyunu (AI Mole Game)

6 yapay zeka modelinin bir kelimeyi tarif ettiği ve aralarındaki "köstebek"i bulmanız gereken günlük sosyal çıkarım oyunu.

## 🎮 Oyun Nasıl Çalışır?

1. Her gün gece yarısı yeni bir oyun oluşturulur
2. 6 AI modeli (Gemini, Claude, ChatGPT, Grok, Llama, DeepSeek) bir kelimeyi tarif eder
3. 5 model **masum kelimeyi**, 1 model **köstebek kelimesini** tarif eder
4. Kullanıcılar konuşmaları okuyarak köstebeği bulmaya çalışır

## 🛠 Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Backend | FastAPI (Python) |
| Frontend | Next.js + Tailwind CSS |
| Database | Supabase (PostgreSQL) |
| AI API | OpenRouter |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |

## 📦 Kurulum

### 1. Supabase Kurulumu

1. [Supabase](https://supabase.com) hesabı oluşturun
2. Yeni proje oluşturun
3. SQL Editor'e gidin ve `supabase_schema.sql` dosyasının içeriğini çalıştırın
4. Project Settings > API bölümünden `URL` ve `anon key` değerlerini alın

### 2. OpenRouter API Key

1. [OpenRouter](https://openrouter.ai) hesabı oluşturun
2. API anahtarı oluşturun

### 3. Backend Deploy (Render)

1. [Render](https://render.com) hesabı oluşturun
2. "New Web Service" > "Build and deploy from Git"
3. Bu repo'yu bağlayın, root directory: `backend`
4. Environment variables ekleyin:
   - `SUPABASE_URL`: Supabase project URL
   - `SUPABASE_KEY`: Supabase anon key
   - `OPENROUTER_API_KEY`: OpenRouter API key
5. Deploy edin ve URL'i not alın

### 4. Frontend Deploy (Vercel)

1. [Vercel](https://vercel.com) hesabı oluşturun
2. "Add New Project" > Bu repo'yu seçin
3. Root directory: `frontend`
4. Environment variable ekleyin:
   - `NEXT_PUBLIC_API_URL`: Render backend URL'iniz
5. Deploy edin

## 🔧 Yerel Geliştirme

### Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# .env dosyası oluşturun
copy .env.example .env
# .env içindeki değerleri doldurun

uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install

# .env.local dosyası oluşturun
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
```

## 📡 API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/daily` | Günün oyun bilgilerini getirir |
| POST | `/api/play_turn` | Tur oynar (PAS veya ELEME) |
| POST | `/api/cron/daily-setup` | Günlük kurulumu tetikler |

### Örnek İstekler

```bash
# Günün oyununu al
curl https://your-backend.onrender.com/api/daily

# Tur oyna
curl -X POST https://your-backend.onrender.com/api/play_turn \
  -H "Content-Type: application/json" \
  -d '{"action": "ELIMINATE", "target_model": "Gemini", "current_state_hash": "abc123"}'
```

## 🎯 Akıllı Önbellek (Smart Cache)

Sistem **maliyet etkinliği** için akıllı önbellek kullanır:

1. Her oyun durumu bir MD5 hash'i ile tanımlanır
2. Aynı durum için ikinci istek geldiğinde, önbellekten döndürülür (API maliyeti: $0)
3. İlk kullanıcıların beklemesini önlemek için 1. tur önceden hesaplanır

## 📝 Lisans

MIT

## 🤝 Katkıda Bulunun

Pull request'ler memnuniyetle karşılanır!
