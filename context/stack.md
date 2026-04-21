# MonkeyDo Tech Stack (AWS-Native)

## Frontend
- **Framework:** Next.js 16 (React 19) with TypeScript
- **Styling:** Tailwind CSS 4
- **Deployment:** **AWS Amplify Hosting**
- **Dev:** `make start` (runs `npm run dev` on port 3000)

## Backend
- **Framework:** FastAPI (Python 3.12+)
- **ORM:** SQLAlchemy 2.0 (async with asyncpg)
- **Migrations:** Alembic
- **Deployment:** **AWS App Runner** (containerized with Docker)
- **Dev:** `make start` (runs `uvicorn app.main:app --reload` on port 8000)

## Database
- **Engine:** PostgreSQL 16
- **Provider:** **AWS RDS** (`oscars-db.cxye2ao0gk53.eu-central-1.rds.amazonaws.com`)
- **Database name:** `postgres` (not a separate monkeydo db)
- **Connection:** Backend connects via `DATABASE_URL` in `.env`

## Infrastructure
- **Storage:** AWS S3 (planned — for processed audio/transcripts)
- **Domain/SSL:** Managed automatically by Amplify and App Runner

## Auth (Planned -- Post-MVP)
- **Provider:** AWS Cognito
- **Current:** Single hardcoded user (`DEFAULT_USER_ID`)

## Matching Logic (Engine Rules)
- **Correct (Green):** Typed word is an exact case-insensitive match.
- **Partial (Yellow):** Shared prefix between typed input and target word covers
  >=50% of the target word's length. e.g. "heutsssss" matches "heute" because
  shared prefix "heut" = 4/5 = 80%. Shown as yellow prefix + red missing chars.
- **Incorrect (Red):** Shared prefix <50%. Input box flashes red and clears.
- **Order:** Typing is order-free. The engine checks the input against **all
  unguessed word slots**. Best coverage wins. Leftmost wins on tie.
- **Status mapping in `word_history`:** `correct` = exact match, `ok` = 50%+
  prefix match, `wrong` = rejected guess.

## Skip Mechanic
- **Tab** -- skip current word: reveal it immediately, not recorded in history.
- **Shift+Tab** -- skip entire sentence: all remaining words reveal, not recorded.

## Sentence Transitions
- When all words in a sentence are revealed, the answer stays visible for **3
  seconds** (timer frozen) before advancing to the next sentence.

## Layout
- **Single-page app.** Sidebar always visible on left. Clicking a lesson loads
  the engine in the right panel -- no page navigation.
