-- ############################################################
-- MonkeyDo Database Schema - Unified Script
-- ############################################################

-- 0. Setup & Extensions
-- Ensures UUID generation and public schema access
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
SET search_path TO public;

/* -- UNCOMMENT THESE IF YOU NEED TO WIPE EVERYTHING AND START OVER:
DROP TABLE IF EXISTS analytics_tips;
DROP TABLE IF EXISTS word_history;
DROP TABLE IF EXISTS game_sessions;
DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS folders;
DROP TABLE IF EXISTS users;
*/


-- 1. Table: users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    is_premium BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 2. Table: folders
CREATE TABLE IF NOT EXISTS folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 3. Table: lessons
-- target_data stores:
--   [{ "index": 0, "sentence_index": 0, "source_word_index": 1, "primary": "Ich", "synonyms": [] }, ...]
-- sentence_index  → groups words into display rows (one sentence at a time)
-- source_word_index → 0-based position of the mapped word in the source sentence
--                     enables word-level EN↔DE alignment and optional reordering
-- source_language / target_language use BCP-47 codes (e.g. "en", "de", "fr", "es").
CREATE TABLE IF NOT EXISTS lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    folder_id UUID REFERENCES folders(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    source_language TEXT NOT NULL DEFAULT 'en',
    target_language TEXT NOT NULL DEFAULT 'de',
    text_source TEXT NOT NULL,
    target_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- 4. Table: game_sessions
CREATE TABLE IF NOT EXISTS game_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID NOT NULL REFERENCES lessons(id),
    user_id UUID NOT NULL REFERENCES users(id),
    difficulty TEXT CHECK (difficulty IN ('easy', 'medium', 'hard')),
    duration_seconds INTEGER CHECK (duration_seconds BETWEEN 60 AND 600),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 5. Table: word_history
CREATE TABLE IF NOT EXISTS word_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    word_index INTEGER NOT NULL,
    typed_word TEXT,                    -- NULL for skipped words
    is_synonym BOOLEAN DEFAULT false,
    status TEXT CHECK (status IN ('correct', 'ok', 'wrong', 'skipped')),
    attempts INTEGER DEFAULT 1,         -- 0 for skipped words
    latency_ms INTEGER                  -- NULL for skipped or pre-filled words
);

-- 6. Table: analytics_tips
CREATE TABLE IF NOT EXISTS analytics_tips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    category TEXT CHECK (category IN ('grammar', 'vocab', 'nuance')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- ############################################################
-- Performance Indexes (Optimized for Soft Deletes)
-- ############################################################

-- Fast lookups for active users/folders
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;
CREATE INDEX idx_folders_active_user ON folders(user_id) WHERE deleted_at IS NULL;

-- Fast lookups for "Home" directory (folder_id is NULL) vs specific folders
CREATE INDEX idx_lessons_home ON lessons(user_id) WHERE folder_id IS NULL AND deleted_at IS NULL;
CREATE INDEX idx_lessons_folder ON lessons(folder_id) WHERE folder_id IS NOT NULL AND deleted_at IS NULL;

-- Faster analytics processing
CREATE INDEX idx_word_history_session_lookup ON word_history(session_id);
CREATE INDEX idx_game_sessions_user_history ON game_sessions(user_id, created_at DESC);
