# 🗺️ MonkeyDo Project Roadmap

This roadmap defines the iterative development of MonkeyDo. Each milestone
represents a functional shift in the application.

---

## Milestone 1: The "Walking Skeleton" (MVP) **Goal:** Establish the end-to-end
pipeline (DB -> API -> UI). A functional translation drill using hardcoded
data.

### Backend (Python/FastAPI)
- [ ] **Task B1.1:** Initialize FastAPI project with SQLAlchemy 2.0 and
Alembic.
- [ ] **Task B1.2:** Implement Core Models (`User`, `Folder`, `Lesson`) as per
`db_schema.md`. The `Lesson` model must represent `target_data` as a JSONB
array of `{ index, sentence_index, source_word_index, primary, synonyms[] }`.
- [ ] **Task B1.3:** Create an Alembic migration that seeds one hardcoded user
(fixed UUID stored as a constant — e.g. `DEFAULT_USER_ID`) to act as the sole
user until Cognito auth is wired up. Also seeds sample German/English lessons
with synonym examples.
- [ ] **Task B1.4:** Implement `GET /sidebar` returning a nested structure:
`{ folders: [{ id, name, lessons: [...] }], root_lessons: [...] }`. Implement
`GET /lessons/{id}` returning `source_language`, `target_language`,
`text_source`, and the full `target_data` array.
- [ ] **Task B1.5:** Implement `POST /games/start`: called on first keypress,
accepts `lesson_id` and `duration_seconds` (user-chosen timer length), creates
and returns a `game_session` row with its `id`.
- [ ] **Task B1.6:** Dockerize application and set up basic deployment config
for AWS App Runner.

### Frontend (Next.js/TS)
- [ ] **Task F1.1:** Initialize Next.js project with Tailwind CSS. Single-page
layout: sidebar fixed on the left, engine panel fills the right. No routing —
clicking a lesson swaps the engine content in-place.
- [ ] **Task F1.2:** Build Sidebar component to render the nested folder/lesson
structure.
- [ ] **Task F1.3:** Build the "Engine" component: Two-row display (English
visible, German hidden/blurred).
- [ ] **Task F1.4:** Implement pre-game UI: user selects timer duration (1–10
min) before starting. First keypress fires `POST /games/start`, stores
`session_id`, and starts the countdown simultaneously.
- [ ] **Task F1.5:** Implement typing logic: single-word input, validate against
the full synonym array (`primary` + `synonyms[]`) across all unguessed words
(order-free). The slot with the highest character overlap (≥50%) wins;
leftmost wins on a tie.
- [ ] **Task F1.6:** Implement synonym reveal UI: on correct match, expand a
vertical list at the word slot showing all valid alternatives. Highlight the
user's typed word in Green; show remaining synonyms in a muted color.
- [ ] **Task F1.6b:** Implement skip mechanic: `Tab` skips the current word
(reveals it, records `status='skipped'`); `Shift+Tab` skips the entire current
sentence. After a skip, the next keypress resumes input for the next unguessed
word.
- [ ] **Task F1.7:** Implement session end: triggers when countdown hits 0 OR
all words are revealed. Both paths call `POST /games/finish`.
- [ ] **Task F1.8:** Implement "Next Sentence" transition when all words in a
row are revealed; advance to the next `sentence_index` group.

---

## Milestone 2: The "AI Material Lab" (Manual Creation) **Goal:** Allow users
to create their own study material via text + AI prompts.

### Backend (Python/FastAPI)
- [ ] **Task B2.1:** Integrate OpenAI Python SDK (`openai` package). Use the
Chat Completions API with `response_format` (structured output / JSON schema)
— no LiteLLM or abstraction layers. API key via `.env`.
- [ ] **Task B2.2:** Implement `POST /lessons/generate` (raw text + prompt +
source/target language -> structured `target_data` JSON). Use OpenAI structured
output to enforce the schema: array of `{ index, sentence_index,
source_word_index, primary, synonyms[] }`. The system prompt instructs the
model to: (1) split text into sentences, (2) translate each word, (3) map each
target word back to its source word via `source_word_index`, (4) populate
`synonyms[]` with interchangeable alternatives.
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

## Milestone 3: The "Dopamine" Update (UI & Polish) **Goal:** Add the
"MonkeyType" feel with colors, animations, and sound.

### Frontend (Next.js/TS)
- [ ] **Task F3.1:** Implement "Blink" animations and state colors: Green
(Correct), Yellow (Partial), Red (Error).
- [ ] **Task F3.2:** Add subtle sound effects for keypresses and correct
submissions.
- [ ] **Task F3.3:** Build the "Difficulty Toggle" (Easy/Med/Hard) to pre-fill
or hide words in the Engine.
- [ ] **Task F3.4:** Implement a countdown timer (1–10 min) that triggers the
end of a session.

---

## Milestone 4: The "Review Loop" (Analytics & AI Coaching) **Goal:** Post-game
data visualization and personalized grammar coaching.

### Backend (Python/FastAPI)
- [ ] **Task B4.1:** Implement `POST /games/finish`: receives
`{ session_id, word_history: [{ word_index, typed_word, is_synonym, status, attempts, latency_ms }] }`.
Persists all `word_history` rows, computes WPM and accuracy, finalizes the session.
- [ ] **Task B4.2:** Build the AI Coaching logic: Send errors and synonym
choices to LLM to generate `analytics_tips` with "nuance" category entries
(e.g., "You used 'traumhaft'—correct, but 'wunderschön' is more common here").
- [ ] **Task B4.3:** Implement `GET /analytics/{lesson_id}`: Aggregate stats
across all attempts of a lesson, including synonym usage breakdown.

### Frontend (Next.js/TS)
- [ ] **Task F4.1:** Build the "Post-Game Summary" screen (WPM, Accuracy,
Missed words list).
- [ ] **Task F4.2:** Implement the "Failure Heatmap": Visual highlights of
target words that caused friction.
- [ ] **Task F4.3:** Display the AI Tutor component: Show grammar tips and
synonym nuance feedback for missed or synonym-matched words.

---

## Milestone 5: The "Deep Import" (Transcription) **Goal:** Automated lesson
creation from YouTube and Podcasts.

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

## Milestone 6: The "Iterative Tutor" (Editing) **Goal:** Ability to refine and
update existing lessons.

### Backend (Python/FastAPI)
- [ ] **Task B6.1:** Implement `PATCH /lessons/{id}` to update text, internal
prompts, or individual synonym lists within `target_data`.
- [ ] **Task B6.2:** Add soft-delete logic (`deleted_at`) for lessons and
folders.

### Frontend (Next.js/TS)
- [ ] **Task F6.1:** Build "Edit Mode" UI: Re-open a lesson in the Material Lab
to tweak, re-generate, or manually edit synonym lists per word.

---

## Milestone 7: The "Organized Brain" (Drag & Drop) **Goal:** Full Zen-inspired
workspace management.

### Frontend (Next.js/TS)
- [ ] **Task F7.1:** Integrate `dnd-kit` to allow reordering of sidebar items.
- [ ] **Task F7.2:** Implement "Drop into Folder" logic.
- [ ] **Task F7.3:** Persist new folder structures to the backend.

---

## Milestone 8: The "Power User" (Shortcuts & Search) **Goal:** Lightning-fast
navigation via keyboard and fuzzy search.

### Frontend (Next.js/TS)
- [ ] **Task F8.1:** Implement "Telescope" command palette (`Cmd+K`) using
Fuse.js.
- [ ] **Task F8.2:** Map global shortcuts: `N` (New), `R` (Reveal), `Space`
(Start), `Arrow` (Skip).

---

## Milestone 9: "Real Users" (Auth — AWS Cognito) **Goal:** Replace the
hardcoded `DEFAULT_USER_ID` with real authenticated users.

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
