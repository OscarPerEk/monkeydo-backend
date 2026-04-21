# 🗄️ MonkeyDo Database Schema Specification

This schema is designed for a high-performance language learning app. It uses **UUIDs** for primary keys, supports **Soft Deletes** (`deleted_at`), and structures lesson targets as **JSONB** to natively support synonym matching and zero-latency frontend validation.

---

## 1. `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique identifier for the user. |
| `email` | String | Unique, Not Null | User's email address for identification. |
| `is_premium` | Boolean | Default: false | Tracks if the user has access to premium AI features. |
| `created_at` | DateTime | Default: now() | When the account was created. |
| `updated_at` | DateTime | Default: now() | When the account was last updated. |
| `deleted_at` | DateTime | Nullable | Used for soft deletion (GDPR/Account deactivation). |

## 2. `folders`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique identifier for the folder. |
| `user_id` | UUID | FK -> users.id, Not Null | Owner of the folder. |
| `name` | String | Not Null | Display name (e.g., "Medical German"). |
| `created_at` | DateTime | Default: now() | When the folder was created. |
| `updated_at` | DateTime | Default: now() | When the folder was last renamed/moved. |
| `deleted_at` | DateTime | Nullable | Soft delete timestamp. |

## 3. `lessons`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique identifier for the lesson. |
| `user_id` | UUID | FK -> users.id, Not Null | Owner of the lesson. |
| `folder_id` | UUID | FK -> folders.id, **Nullable** | If NULL, lesson appears in "Home". |
| `title` | String | Not Null | Name of the lesson/video title. |
| `source_language` | String | Not Null, Default: 'en' | BCP-47 language code for the source (e.g. "en", "fr"). |
| `target_language` | String | Not Null, Default: 'de' | BCP-47 language code for the language being learned (e.g. "de", "es"). |
| `text_source` | Text | Not Null | Row A: The full source text. Frontend splits into sentences/chunks for display. |
| `target_data` | JSONB | Not Null | Row B: Flat array of all target words. Schema: `{ index, sentence_index, source_word_index, primary, synonyms[] }`. `sentence_index` groups words into rows. `source_word_index` maps each target word to its 0-based position in the corresponding source sentence, enabling word-level EN↔DE alignment and optional sentence reordering. |
| `created_at` | DateTime | Default: now() | When the lesson was generated/created. |
| `updated_at` | DateTime | Default: now() | Last edit timestamp. |
| `deleted_at` | DateTime | Nullable | Soft delete timestamp. |

## 4. `game_sessions`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique ID for a single play-through. |
| `lesson_id` | UUID | FK -> lessons.id, Not Null | Which lesson was played. |
| `user_id` | UUID | FK -> users.id, Not Null | Who played the game. |
| `difficulty` | String | "easy", "medium", "hard" | The difficulty setting chosen. |
| `duration_seconds`| Integer | 60 - 600 | Length of the test (1 to 10 mins). |
| `created_at` | DateTime | Default: now() | When the game was played. |

## 5. `word_history`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique ID for the event. |
| `session_id` | UUID | FK -> game_sessions.id, Not Null | Link to the parent game session. |
| `word_index` | Integer | Not Null | Position of the word in the sentence array. |
| `typed_word` | String | **Nullable** | The actual word the user typed. NULL if the word was skipped. |
| `is_synonym` | Boolean | Default: false | True if they matched a synonym instead of the primary word. |
| `status` | String | "correct", "ok", "wrong", "skipped" | Result: `correct`=exact match, `ok`=≥50% prefix match, `wrong`=rejected guess, `skipped`=Tab/Shift+Tab used (never attempted). |
| `attempts` | Integer | Default: 1 | Tries before correct submission. 0 for skipped words. |
| `latency_ms` | Integer | **Nullable** | Speed of the correct submission in ms. NULL for skipped or pre-filled words. |

## 6. `analytics_tips`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default: gen_random_uuid() | Unique identifier for the tip. |
| `session_id` | UUID | FK -> game_sessions.id, Not Null | Link to the specific game performance. |
| `content` | Text | Not Null | AI-generated Markdown tips/explanations. |
| `category` | String | "grammar", "vocab", "nuance" | Type of feedback provided. |
| `created_at` | DateTime | Default: now() | When the feedback was generated. |

---

## 🚦 System Rules
1. **Soft Deletes:** Never `DELETE` rows. Set `deleted_at = now()` to hide items from the UI.
2. **Home Directory:** A `lesson` with `folder_id = NULL` is considered a root-level item.
3. **Session Logic:** A `game_session` is immutable once the time runs out.
4. **AI Latency:** `analytics_tips` are generated asynchronously after `game_session` is finalized, leveraging the `is_synonym` flags to give nuanced feedback.
