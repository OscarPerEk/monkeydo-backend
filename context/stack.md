# MonkeyDo Tech Stack (AWS-Native)

## Frontend
- **Framework:** Next.js (React)
- **Deployment:** **AWS Amplify Hosting**. 
    - *Why:* It's the AWS version of Vercel. It connects to your GitHub, builds
    your Next.js app, and hosts it on a global CDN automatically.

## Backend
- **Framework:** FastAPI (Python 3.12+)
- **Deployment:** **AWS App Runner**.
    - *Why:* It's the simplest way to run a container. It handles the Load
    Balancer and "Auto-scaling" out of the box. You don't have to manage
    servers.

## Database
- **Engine:** PostgreSQL 16
- **Provider:** **AWS RDS**.
    - *Why:* Reliable, managed backups, and fits in the Free Tier for 12
    months.

## Infrastructure
- **Storage:** AWS S3 (For storing processed audio/transcripts later).
- **Domain/SSL:** Managed automatically by Amplify and App Runner.

## Auth (Planned — Post-MVP)
- **Provider:** AWS Cognito
    - *Why:* Native to the AWS stack, generous free tier, integrates cleanly
    with App Runner and RDS. Not needed for MVP (single hardcoded user), but
    the architecture should leave a clean seam to add it later.

## Matching Logic (Engine Rules)
- **Correct (Green):** Typed word is an exact match to `primary` or any entry
in `synonyms[]`.
- **Partial / Found (Yellow):** ≥50% of characters overlap with the best
unguessed candidate. The word is considered **found** (accepted) at this
threshold.
- **Incorrect (Red):** <50% overlap. Input box flashes red and clears.
- **Order:** Typing is order-free. The engine checks the input against **all
unguessed word slots**. The slot with the highest character overlap (≥50%)
wins. If multiple slots tie, the leftmost (lowest index) is selected.
- **Status mapping in `word_history`:** `correct` = exact match, `ok` = 50%+
prefix match, `wrong` = rejected guess, `skipped` = word was skipped.

## Skip Mechanic
- **Tab** — skip current word: reveal it immediately, advance to next word.
  Recorded as `status='skipped'`, `typed_word=NULL`, `latency_ms=NULL`, `attempts=0`.
  Next keypress resumes input for the next unguessed word.
- **Shift+Tab** — skip entire current sentence: all remaining unguessed words in
  the row reveal at once, all recorded as `status='skipped'`. Advances to next
  sentence.

## Layout
- **Single-page app.** Sidebar is always visible on the left. Clicking a lesson
  loads the engine in the right panel — no page navigation.
