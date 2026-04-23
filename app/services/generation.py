import logging
import re

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config import settings

logger = logging.getLogger(__name__)

CLEAN_PROMPT = """\
You are a text preparation assistant for a language learning app.

You will receive German text (possibly with typos or formatting issues).

Your job:
1. Fix any spelling or grammar errors in the German text.
2. Split the text into SHORT chunks using | as delimiter.
3. Each chunk should be a small, typeable snippet (3-8 words ideally).
4. Split at logical points: subclauses, commas, conjunctions, or natural pauses.
5. It's OK to split mid-sentence if the sentence is long.
6. Keep the original meaning and style intact.
7. Do NOT add or remove content — only fix errors and insert | delimiters.
8. Generate a short, descriptive title (2-5 words) that captures the topic.

Example input:
"Ich bin gestern in die Stadt gefahren weil ich einen neuen Laptop kaufen wollte. Der Laden hatte leider geschlossen also bin ich ins Café gegangen."

Example output:
"Ich bin gestern in die Stadt gefahren | weil ich einen neuen Laptop kaufen wollte. | Der Laden hatte leider geschlossen | also bin ich ins Café gegangen."
"""

TRANSLATE_PROMPT = """\
You are a translation assistant for a language learning app.

You will receive German text chunks separated by |.
Translate each chunk to English, keeping the SAME | structure.
Each German chunk must map 1:1 to an English chunk.
Keep translations natural but faithful to the original.

{user_instructions}
"""


class CleanedText(BaseModel):
    title: str
    cleaned_text: str  # German text with | delimiters


class TranslatedText(BaseModel):
    english_text: str  # English text with | delimiters


class GeneratedTargetWord(BaseModel):
    index: int
    sentence_index: int
    word: str


class GeneratedLesson(BaseModel):
    title: str
    text_source: str
    target_data: list[GeneratedTargetWord]


def _build_target_data(german_chunks: list[str]) -> list[GeneratedTargetWord]:
    """Deterministically build target_data from German chunks. No LLM needed."""
    words = []
    global_index = 0
    for sentence_idx, chunk in enumerate(german_chunks):
        # Split chunk into words, strip punctuation from each word
        for token in chunk.split():
            clean = re.sub(r"[.,;:!?\"'()…\-–—]", "", token).strip()
            if not clean:
                continue
            words.append(GeneratedTargetWord(
                index=global_index,
                sentence_index=sentence_idx,
                word=clean,
            ))
            global_index += 1
    return words


async def generate_lesson(german_text: str, prompt: str) -> GeneratedLesson:
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    model = settings.openai_model

    # Step 1: Clean and split German text
    logger.info("Step 1: Cleaning and splitting German text...")
    clean_response = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": CLEAN_PROMPT},
            {"role": "user", "content": german_text},
        ],
        response_format=CleanedText,
    )
    cleaned = clean_response.choices[0].message.parsed
    logger.info("Step 1 done: title=%s, chunks=%d", cleaned.title, cleaned.cleaned_text.count("|") + 1)

    # Step 2: Translate chunks to English
    user_instructions = f"Additional instructions from the user:\n{prompt}" if prompt.strip() else ""
    translate_system = TRANSLATE_PROMPT.format(user_instructions=user_instructions)

    logger.info("Step 2: Translating chunks...")
    translate_response = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": translate_system},
            {"role": "user", "content": cleaned.cleaned_text},
        ],
        response_format=TranslatedText,
    )
    translated = translate_response.choices[0].message.parsed
    logger.info("Step 2 done: english=%s", translated.english_text[:80])

    # Build the lesson deterministically
    german_chunks = [c.strip() for c in cleaned.cleaned_text.split("|") if c.strip()]
    english_text = translated.english_text

    target_data = _build_target_data(german_chunks)

    return GeneratedLesson(
        title=cleaned.title,
        text_source=english_text,
        target_data=target_data,
    )
