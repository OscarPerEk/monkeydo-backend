# Project: MonkeyDo (Active Language Learning)

## 🎯 The Vision **MonkeyDo** is a high-performance "Active Recall" language
learning platform. It bridges the gap between passive content consumption
(watching YouTube/listening to podcasts) and active fluency. By combining the
minimalist "flow state" of **MonkeyType** with the organizational beauty of the
**Zen Browser**, it forces users to physically produce language under pressure.

**Core Philosophy:** * **Active > Passive:** Typing a translation is superior
to multiple-choice.
* **Context is King:** Users learn best using material *they* care about
(custom uploads).
* **Zero Latency:** The interface must feel like a professional tool—instant,
snappy, and distraction-free.
* **Fluidity in Language:** Language isn't rigid. The app inherently supports
and teaches synonyms, rewarding any valid translation without breaking the
user's flow.

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
* **The Interface:** Two primary rows, utilizing vertical space for
alternatives.
    * **Top Row (Source):** English text (Always visible).
    * **Bottom Row (Target):** German translation (Initially hidden/blurred).
* **The Gameplay (Synonym Matching):**
    * **Input:** A single-word input box. Submission on `Space` or `Enter`.
    * **Matching:** Words can be guessed out of order. The engine checks the
    input against an array of acceptable words (primary + synonyms) for each
    position.
* **The Reveal (Vertical List UI):**
    * When a user successfully types a valid word, the position reveals.
    * If there are synonyms, they expand vertically downwards from that word
    slot in Row B (e.g., a vertical stack showing *wunderschöner*,
    *traumhafter*, *schöner*).
    * The exact word the user typed highlights **Green**, while the other valid
    alternatives remain visible in a subtle, muted color for passive vocabulary
    building.
* **Difficulty Levels:**
    * **Easy:** ~33% of the target row is pre-filled.
    * **Medium:** ~66% of the target row is hidden.
    * **Hard:** 100% of the target row is hidden.
* **Visual Feedback:**
    * **Correct:** Word/Synonym lights up **Green**.
    * **Partial (>=50% match):** Word glows **Yellow**.
    * **Incorrect:** Input box flashes **Red** and clears.

### 3. The AI Material Lab (Lesson Creation)
* **Ingestion:** Import via YouTube URL, Audio file, or manual Text.
* **Processing:** * AI transcribes the source.
    * User provides a **Prompt** (e.g., "Focus on Dative verbs").
    * AI generates the translation as a structured JSON array, providing a
    primary word and a list of valid synonyms for verbs, adjectives, and
    interchangeable nouns/pronouns.
* **Version Control:** A list of "Generations" at the bottom to tweak prompts
and switch versions.

### 4. Post-Session Analytics & Coaching
* **Stats:** WPM (Words Per Minute), Accuracy, and "Failure Heatmap".
* **AI Tutor:** * Explains grammar patterns based on errors.
    * Analyzes synonym choices (e.g., *"You used 'traumhafter', which is
    correct, but 'wunderschöner' is slightly more common here!"*).
