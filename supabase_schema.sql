-- =====================================================
-- AI MOLE GAME - SUPABASE VERITABANI ŞEMASI
-- =====================================================
-- Bu SQL'i Supabase SQL Editor'de çalıştırın

-- 1. Kelime Çiftleri Tablosu
CREATE TABLE IF NOT EXISTS word_pairs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category TEXT NOT NULL,
  innocent_word TEXT NOT NULL,
  mole_word TEXT NOT NULL,
  difficulty INT DEFAULT 3 CHECK (difficulty >= 1 AND difficulty <= 5),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Günlük Kurulum Tablosu
CREATE TABLE IF NOT EXISTS daily_setup (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE UNIQUE NOT NULL,
  word_pair_id UUID REFERENCES word_pairs(id) ON DELETE CASCADE,
  mole_model TEXT NOT NULL,
  turn_order JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Oyun Durumları Tablosu (Akıllı Önbellek)
CREATE TABLE IF NOT EXISTS game_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  state_hash TEXT UNIQUE NOT NULL,
  date DATE NOT NULL,
  round_number INT NOT NULL,
  remaining_models JSONB NOT NULL,
  action TEXT NOT NULL,
  eliminated_model TEXT,
  dialogues JSONB NOT NULL DEFAULT '[]',
  game_over BOOLEAN DEFAULT FALSE,
  winner TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_game_states_hash ON game_states(state_hash);
CREATE INDEX IF NOT EXISTS idx_game_states_date ON game_states(date);
CREATE INDEX IF NOT EXISTS idx_daily_setup_date ON daily_setup(date);

-- =====================================================
-- ÖRNEK VERİ - Kelime Çiftleri
-- =====================================================

INSERT INTO word_pairs (category, innocent_word, mole_word, difficulty) VALUES
-- Spor
('Spor', 'Ronaldo', 'Messi', 3),
('Spor', 'Basketbol', 'Voleybol', 2),
('Spor', 'Şampiyon', 'Finalist', 4),

-- Teknoloji
('Teknoloji', 'iPhone', 'Android', 2),
('Teknoloji', 'Python', 'JavaScript', 3),
('Teknoloji', 'Tesla', 'BMW', 3),

-- Yiyecek
('Yiyecek', 'Pizza', 'Hamburger', 2),
('Yiyecek', 'Kahve', 'Çay', 2),
('Yiyecek', 'Çikolata', 'Vanilya', 3),

-- Şehirler
('Şehirler', 'İstanbul', 'Ankara', 3),
('Şehirler', 'Paris', 'Londra', 3),
('Şehirler', 'Tokyo', 'Seul', 4),

-- Filmler
('Filmler', 'Matrix', 'Inception', 4),
('Filmler', 'Star Wars', 'Star Trek', 4),
('Filmler', 'Batman', 'Superman', 3),

-- Müzik
('Müzik', 'Rock', 'Pop', 2),
('Müzik', 'Piyano', 'Gitar', 2),
('Müzik', 'Mozart', 'Beethoven', 5),

-- Hayvanlar
('Hayvanlar', 'Köpek', 'Kedi', 2),
('Hayvanlar', 'Aslan', 'Kaplan', 3),
('Hayvanlar', 'Kartal', 'Şahin', 4),

-- Mevsimler/Doğa
('Doğa', 'Yaz', 'Kış', 2),
('Doğa', 'Güneş', 'Ay', 3),
('Doğa', 'Okyanus', 'Deniz', 4),

-- Meslekler
('Meslekler', 'Doktor', 'Hemşire', 3),
('Meslekler', 'Avukat', 'Hakim', 4),
('Meslekler', 'Mühendis', 'Mimar', 4);

-- =====================================================
-- RLS (Row Level Security) - Opsiyonel
-- =====================================================
-- Eğer public erişim istiyorsanız RLS'i disable bırakabilirsiniz
-- ALTER TABLE word_pairs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE daily_setup ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE game_states ENABLE ROW LEVEL SECURITY;

-- Public okuma izni için policy
-- CREATE POLICY "Public read access" ON word_pairs FOR SELECT USING (true);
-- CREATE POLICY "Public read access" ON daily_setup FOR SELECT USING (true);
-- CREATE POLICY "Public read access" ON game_states FOR SELECT USING (true);
