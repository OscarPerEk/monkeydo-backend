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
`db_schema.md`.
- [ ] **Task B1.3:** Create an Alembic migration to seed the DB with sample
German/English lessons.
- [ ] **Task B1.4:** Implement `GET /sidebar` (Titles/Folders) and `GET
/lessons/{id}` (Game Text).
- [ ] **Task B1.5:** Dockerize application and set up basic deployment config
for AWS App Runner.

### Frontend (Next.js/TS)
- [ ] **Task F1.1:** Initialize Next.js project with Tailwind CSS and a
"Zen-minimalist" layout.
- [ ] **Task F1.2:** Build Sidebar component to render the nested folder/lesson
structure.
- [ ] **Task F1.3:** Build the "Engine" component: Two-row display (English
visible, German hidden).
- [ ] **Task F1.4:** Implement basic typing logic: Single word input, reveal on
match.
- [ ] **Task F1.5:** Implement "Next Sentence" transition when a row is fully
revealed.

---

## Milestone 2: The "AI Material Lab" (Manual Creation) **Goal:** Allow users
to create their own study material via text + AI prompts.

### Backend (Python/FastAPI)
- [ ] **Task B2.1:** Integrate LLM API (OpenAI/Gemini) for text-to-drill
generation.
- [ ] **Task B2.2:** Implement `POST /lessons/generate` (Raw text + Prompt ->
Row A/B pairs).
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
- [ ] **Task B8.1:** Implement `POST /games/finish`: Receive session results
(WPM, Accuracy, Word History).
- [ ] **Task B8.2:** Build the AI Coaching logic: Send errors to LLM to
generate `analytics_tips`.
- [ ] **Task B8.3:** Implement `GET /analytics/{lesson_id}`: Aggregate stats
across all attempts of a lesson.

### Frontend (Next.js/TS)
- [ ] **Task F8.1:** Build the "Post-Game Summary" screen (WPM, Accuracy,
Missed words list).
- [ ] **Task F8.2:** Implement the "Failure Heatmap": Visual highlights of Row
B words that caused friction.
- [ ] **Task F8.3:** Display the AI Tutor component: Show grammar tips and
synonyms for missed nouns.

---

## Milestone 5: The "Deep Import" (Transcription) **Goal:** Automated lesson
creation from YouTube and Podcasts.

### Backend (Python/FastAPI)
- [ ] **Task B4.1:** Integrate a Transcription API (Whisper/Supadata) to handle
URLs.
- [ ] **Task B4.2:** Build an async task flow to handle the delay of
transcribing long audio.
- [ ] **Task B4.3:** Implement file upload endpoint for local MP3/WAV imports.

### Frontend (Next.js/TS)
- [ ] **Task F4.1:** Add "Import from Link/File" modal to the sidebar.
- [ ] **Task F4.2:** Implement loading states for lessons currently being
processed by AI.

---

## Milestone 6: The "Iterative Tutor" (Editing) **Goal:** Ability to refine and
update existing lessons.

### Backend (Python/FastAPI)
- [ ] **Task B5.1:** Implement `PATCH /lessons/{id}` to update text or internal
prompts.
- [ ] **Task B5.2:** Add soft-delete logic (`deleted_at`) for lessons and
folders.

### Frontend (Next.js/TS)
- [ ] **Task F5.1:** Build "Edit Mode" UI: Re-open a lesson in the Material Lab
to tweak and re-generate.

---

## Milestone 7: The "Organized Brain" (Drag & Drop) **Goal:** Full Zen-inspired
workspace management.

### Frontend (Next.js/TS)
- [ ] **Task F6.1:** Integrate `dnd-kit` to allow reordering of sidebar items.
- [ ] **Task F6.2:** Implement "Drop into Folder" logic.
- [ ] **Task F6.3:** Persist new folder structures to the backend.

---

## Milestone 8: The "Power User" (Shortcuts & Search) **Goal:** Lightning-fast
navigation via keyboard and fuzzy search.

### Frontend (Next.js/TS)
- [ ] **Task F7.1:** Implement "Telescope" command palette (`Cmd+K`) using
Fuse.js.
- [ ] **Task F7.2:** Map global shortcuts: `N` (New), `R` (Reveal), `Space`
(Start), `Arrow` (Skip).

