# 🗄️ MonkeyDo Database Schema Specification

This schema is designed for a high-performance language learning app. It uses
**UUIDs** for primary keys, supports **Soft Deletes** (`deleted_at`), and
follows a flexible structure for lessons (Home vs. Folders).

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
| `text_source` | Text | Not Null | Row A: The source text (e.g., English). |
| `text_target` | Text | Not Null | Row B: The correct translation (e.g., German). |
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
| `word_index` | Integer | Not Null | Position of the word in the sentence. |
| `word` | String | Not Null | The word itself. |
| `status` | String | "correct", "ok", "wrong" | The result of the guess. |
| `attempts` | Integer | Default: 1 | How many tries before correct submission. |
| `latency_ms` | Integer | Not Null | Speed of the correct submission. |

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
4. **AI Latency:** `analytics_tips` are generated asynchronously after `game_session` is finalized.
