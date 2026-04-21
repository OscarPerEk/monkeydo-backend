from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config import settings

SYSTEM_PROMPT = """\
You are a language learning assistant for MonkeyDo, a typing-based language learning app.

You will receive German text and an optional user prompt. Your job:

1. Generate an English translation of the German text as `text_source`.
2. Split the German text into individual words, grouped by sentence, as `target_data`.
3. Generate a short lesson `title` (2-5 words).

Rules for `target_data`:
- Each word is a separate entry with fields: `index`, `sentence_index`, `word`.
- `index` is a global 0-based counter across ALL words in ALL sentences.
- `sentence_index` is the 0-based sentence number.
- Punctuation attached to words should be removed (e.g. "gut." becomes "gut").
- Keep capitalization as-is in the German text.

The user's prompt may ask you to:
- Modify the German text (simplify, make more formal, etc.)
- Adjust the English translation (simpler, British English, etc.)
- Change the topic or style
- Any other creative instruction

Follow the user's prompt. If no prompt is given, just translate faithfully.\
"""


class GeneratedTargetWord(BaseModel):
    index: int
    sentence_index: int
    word: str


class GeneratedLesson(BaseModel):
    title: str
    text_source: str
    target_data: list[GeneratedTargetWord]


async def generate_lesson(german_text: str, prompt: str) -> GeneratedLesson:
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    user_message = f"German text:\n{german_text}"
    if prompt.strip():
        user_message += f"\n\nUser instructions:\n{prompt}"

    response = await client.beta.chat.completions.parse(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        response_format=GeneratedLesson,
    )

    return response.choices[0].message.parsed
