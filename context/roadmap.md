# MonkeyDo Project Roadmap

This roadmap defines the iterative development of MonkeyDo. Each milestone
represents a functional shift in the application.

---

## Milestone 1: The "Walking Skeleton" (MVP)
**Goal:** Establish the end-to-end pipeline (DB -> API -> UI). A functional
translation drill using hardcoded data.

### Backend (Python/FastAPI)
- [x] **Task B1.1:** Initialize FastAPI project with SQLAlchemy 2.0 and Alembic.
- [x] **Task B1.2:** Implement Core Models (`User`, `Folder`, `Lesson`,
`GameSession`, `WordHistory`) as per `db_schema.md`. The `Lesson` model
represents `target_data` as a JSONB array of `{ index, sentence_index,
source_word_index, word }`.
- [x] **Task B1.3:** Create an Alembic migration that seeds one hardcoded user
(fixed UUID: `DEFAULT_USER_ID`) to act as the sole user until Cognito auth is
wired up.
- [x] **Task B1.4:** Implement `GET /sidebar` returning a nested structure:
`{ folders: [{ id, name, lessons: [...] }], root_lessons: [...] }`. Implement
`GET /lessons/{id}` returning `text_source` and the full `target_data` array.
- [x] **Task B1.5:** Implement `POST /games/start` and `POST /games/finish`.
- [ ] **Task B1.6:** Dockerize application and set up basic deployment config
for AWS App Runner.

### Frontend (Next.js/TS)
- [x] **Task F1.1:** Initialize Next.js project with Tailwind CSS. Single-page
layout: sidebar fixed on the left, engine panel fills the right.
- [x] **Task F1.2:** Build Sidebar component to render the nested folder/lesson
structure.
- [x] **Task F1.3:** Build the "Engine" component: Two-row display (English
visible, German hidden/blurred).
- [x] **Task F1.4:** Implement pre-game UI: first keypress fires
`POST /games/start`, stores `session_id`, and starts the countdown.
- [x] **Task F1.5:** Implement typing logic: single-word input, validate using
shared-prefix matching (>=50% of target word). Case-insensitive. Best coverage
wins; leftmost wins on a tie.
- [x] **Task F1.6:** Implement word reveal UI: exact match shows green, partial
match shows correct prefix in yellow + missing chars in red.
- [x] **Task F1.6b:** Implement skip mechanic: `Tab` skips the current word
(reveals it); `Shift+Tab` skips the entire current sentence. Skipped words are
not recorded in history.
- [x] **Task F1.7:** Implement session end: triggers when countdown hits 0 OR
all words are revealed. Both paths call `POST /games/finish`.
- [x] **Task F1.8:** Implement "Next Sentence" transition with 3-second pause
(timer frozen) when all words in a row are revealed, then advance to next
sentence.

### Simplification Pivot (2026-04-21)
The following were **intentionally removed** from the original MVP plan:
- **Synonyms:** Removed from `target_data` and matching logic. Goal is to learn
  exact writing style, not alternatives.
- **`source_language` / `target_language`:** Removed from lessons table and API.
- **`is_synonym` field:** Removed from `word_history`.
- **`skipped` status:** Skipped words are no longer tracked in history.
- **`typed_word` / `latency_ms` nullable:** Now NOT NULL in the DB.

---

## Milestone 2: The "AI Material Lab" (Manual Creation)
**Goal:** Allow users to create their own study material via text + AI prompts.

### Backend (Python/FastAPI)
- [ ] **Task B2.1:** Integrate OpenAI Python SDK. Use structured output to
enforce the simplified schema: array of `{ index, sentence_index,
source_word_index, word }`.
- [ ] **Task B2.2:** Implement `POST /lessons/generate` (raw text + prompt ->
structured `target_data` JSON).
- [ ] **Task B2.3:** Implement `POST /lessons` to save chosen generations.
- [ ] **Task B2.4:** Implement Generation Versioning: Store/retrieve multiple
AI "takes" for one lesson.

### Frontend (Next.js/TS)
- [ ] **Task F2.1:** Build the `/create` page with source text input and prompt
box.
- [ ] **Task F2.2:** Build the "Generation History" selector to toggle between
AI versions.
- [ ] **Task F2.3:** Implement the "Save Lesson" flow to persist AI output to
the sidebar.

---

## Milestone 3: The "Dopamine" Update (UI & Polish)
**Goal:** Add the "MonkeyType" feel with colors, animations, and sound.

### Frontend (Next.js/TS)
- [ ] **Task F3.1:** Implement "Blink" animations and state colors: Green
(Correct), Yellow (Partial), Red (Error).
- [ ] **Task F3.2:** Add subtle sound effects for keypresses and correct
submissions.
- [ ] **Task F3.3:** Build the "Difficulty Toggle" (Easy/Med/Hard) to pre-fill
or hide words in the Engine.
- [ ] **Task F3.4:** Implement a countdown timer (1-10 min) that triggers the
end of a session.

---

## Milestone 4: The "Review Loop" (Analytics & AI Coaching)
**Goal:** Post-game data visualization and personalized grammar coaching.

### Backend (Python/FastAPI)
- [ ] **Task B4.1:** Build the AI Coaching logic: Send errors to LLM to
generate `analytics_tips`.
- [ ] **Task B4.2:** Implement `GET /analytics/{lesson_id}`: Aggregate stats
across all attempts of a lesson.

### Frontend (Next.js/TS)
- [ ] **Task F4.1:** Build the "Post-Game Summary" screen (WPM, Accuracy,
Missed words list).
- [ ] **Task F4.2:** Implement the "Failure Heatmap": Visual highlights of
target words that caused friction.
- [ ] **Task F4.3:** Display the AI Tutor component: Show grammar tips for
missed words.

---

## Milestone 5: The "Deep Import" (Transcription)
**Goal:** Automated lesson creation from YouTube and Podcasts.

### Backend (Python/FastAPI)
- [ ] **Task B5.1:** Integrate a Transcription API (Whisper/Supadata) to handle
URLs.
- [ ] **Task B5.2:** Build an async task flow to handle the delay of
transcribing long audio.
- [ ] **Task B5.3:** Implement file upload endpoint for local MP3/WAV imports.

### Frontend (Next.js/TS)
- [ ] **Task F5.1:** Add "Import from Link/File" modal to the sidebar.
- [ ] **Task F5.2:** Implement loading states for lessons currently being
processed by AI.

---

## Milestone 6: The "Iterative Tutor" (Editing)
**Goal:** Ability to refine and update existing lessons.

### Backend (Python/FastAPI)
- [ ] **Task B6.1:** Implement `PATCH /lessons/{id}` to update text or
`target_data`.
- [ ] **Task B6.2:** Add soft-delete logic (`deleted_at`) for lessons and
folders.

### Frontend (Next.js/TS)
- [ ] **Task F6.1:** Build "Edit Mode" UI: Re-open a lesson in the Material Lab
to tweak or re-generate.

---

## Milestone 7: The "Organized Brain" (Drag & Drop)
**Goal:** Full Zen-inspired workspace management.

### Frontend (Next.js/TS)
- [ ] **Task F7.1:** Integrate `dnd-kit` to allow reordering of sidebar items.
- [ ] **Task F7.2:** Implement "Drop into Folder" logic.
- [ ] **Task F7.3:** Persist new folder structures to the backend.

---

## Milestone 8: The "Power User" (Shortcuts & Search)
**Goal:** Lightning-fast navigation via keyboard and fuzzy search.

### Frontend (Next.js/TS)
- [ ] **Task F8.1:** Implement "Telescope" command palette (`Cmd+K`) using
Fuse.js.
- [ ] **Task F8.2:** Map global shortcuts: `N` (New), `R` (Reveal), `Space`
(Start), `Arrow` (Skip).

---

## Milestone 9: "Real Users" (Auth -- AWS Cognito)
**Goal:** Replace the hardcoded `DEFAULT_USER_ID` with real authenticated users.

### Backend (Python/FastAPI)
- [ ] **Task B9.1:** Set up AWS Cognito User Pool. Configure App Client for
the Next.js frontend.
- [ ] **Task B9.2:** Add JWT validation middleware to FastAPI. Decode Cognito
tokens and extract `user_id` on every protected request.
- [ ] **Task B9.3:** Replace all hardcoded `DEFAULT_USER_ID` references with
the authenticated user's ID from the JWT.

### Frontend (Next.js/TS)
- [ ] **Task F9.1:** Integrate AWS Amplify Auth (Cognito SDK) for
sign-up/sign-in flows.
- [ ] **Task F9.2:** Add auth guards: redirect unauthenticated users to login.
- [ ] **Task F9.3:** Pass Cognito JWT as `Authorization: Bearer` header on all
API calls.
