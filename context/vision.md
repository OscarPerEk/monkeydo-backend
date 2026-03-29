# Project: MonkeyDo (Active Language Learning)

## 🎯 The Vision
**MonkeyDo** is a high-performance "Active Recall" language
learning platform. It bridges the gap between passive content consumption
(watching YouTube/listening to podcasts) and active fluency. By combining the
minimalist "flow state" of **MonkeyType** with the organizational beauty of the
**Zen Browser**, it forces users to physically produce language under pressure.

**Core Philosophy:** 
* **Active > Passive:** Typing a translation is superior
to multiple-choice.
* **Context is King:** Users learn best using material *they* care about
(custom uploads).
* **Zero Latency:** The interface must feel like a professional tool—instant,
snappy, and distraction-free.

---

## 🛠 Tech Stack
* **Backend:** Python (FastAPI) – Handling AI orchestration, transcription, and
data persistence.
* **Frontend:** JavaScript/TypeScript (Next.js/React) – High-performance UI and
"MonkeyType" engine logic.
* **Styling:** Tailwind CSS – For a minimalist, "Pro" aesthetic.

---

## 🏗 Core System Architecture

### 1. The "Zen" Workspace (Sidebar Navigation)
* **Structure:** A vertical sidebar on the right/left (inspired by Zen
Browser).
* **Hierarchy:** Nested Folder/Item system. 
    * *Example:* `Folder: Medical German` -> `Lesson: Cardiology Terms`.
* **UX:** Drag-and-drop reordering; right-click context menus for
creating/editing lessons.
* **Account:** Bottom-anchored settings icon for profile and premium tier
management.

### 2. The "MonkeyType" Engine (The Game)
* **The Interface:** Two rows.
    * **Top Row (Source):** English text (Always visible).
    * **Bottom Row (Target):** German translation (Initially hidden/blurred).
* **The Gameplay:**
    * **Input:** A single-word input box. Submission on `Space` or `Enter`.
    * **Matching:** Words can be guessed out of order. If a typed word matches
    any word in the target sentence, that word "reveals" in the bottom row.
* **Difficulty Levels:**
    * **Easy:** ~33% of the target row is pre-filled.
    * **Medium:** ~66% of the target row is hidden.
    * **Hard:** 100% of the target row is hidden.
* **Visual Feedback (Dopamine Loop):**
    * **Correct:** Word blinks **Green**.
    * **Partial (>=50% match):** Word glows **Yellow**.
    * **Incorrect:** Input box flashes **Red** and clears.

### 3. The AI Material Lab (Lesson Creation)
* **Ingestion:** Import via YouTube URL, Audio file, or manual Text.
* **Processing:** * AI transcribes the source.
    * User provides a **Prompt** to tell the AI the focus (e.g., "Focus on
    Dative verbs" or "Use Gen-Z slang").
* **Version Control:**
    * A list of "Generations" at the bottom. Users can tweak prompts and switch
    between different AI-generated versions of the same lesson.

### 4. Post-Session Analytics & Coaching
* **Stats:** WPM (Words Per Minute), Accuracy, and "Failure Heatmap" (words
that caused the most friction).
* **AI Tutor:** * Explains grammar patterns based on errors (e.g., "You
consistently missed the feminine article here").
    * Provides nuances/synonyms for nouns that were missed.
