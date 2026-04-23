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
2. Split the text into chunks using | as delimiter.
3. Each chunk should be a meaningful phrase or clause (5-12 words typically).
4. Split at natural clause boundaries: before conjunctions (weil, dass, aber, also, wenn), at commas, or between sentences.
5. Keep full subclauses together — do NOT split in the middle of a clause.
6. Short sentences (under 10 words) should stay as one chunk, not be split further.
7. Keep the original meaning and style intact.
8. Do NOT add or remove content — only fix errors and insert | delimiters.
9. Generate a short, descriptive title (2-5 words) that captures the topic.

Example input:
"Ich bin gestern in die Stadt gefahren weil ich einen neuen Laptop kaufen wollte. Der Laden hatte leider geschlossen also bin ich ins Café gegangen und habe einen Kaffee getrunken."

Example output:
"Ich bin gestern in die Stadt gefahren | weil ich einen neuen Laptop kaufen wollte. | Der Laden hatte leider geschlossen | also bin ich ins Café gegangen und habe einen Kaffee getrunken."
"""

TRANSLATE_PROMPT = """\
You are a translation assistant for a language learning app.

You will receive German text chunks separated by |.
Translate each chunk to English, keeping the SAME | structure.
Each German chunk must map 1:1 to an English chunk.
Keep translations natural but faithful to the original.

{user_instructions}
"""

VERIFY_PROMPT = """\
You are a quality checker for a language learning app.

You will receive German chunks and English chunks separated by |.
Each German chunk should correspond 1:1 with its English chunk at the same position.

Check for these issues:
1. Misaligned translations (German chunk N doesn't match English chunk N)
2. Missing or extra chunks on either side
3. Translation errors or unnatural phrasing

If there are issues, return corrected versions of BOTH the German and English text (with | delimiters).
If everything looks good, return the input unchanged.

IMPORTANT: The number of | delimiters must be EXACTLY the same in both german_text and english_text.
"""

EXCLUDE_PROMPT = """\
You are a word filtering assistant for a language learning app.

You will receive a list of German words and user instructions about which words to exclude from practice.

Return the list of words that should be EXCLUDED (not practiced). These are typically:
- Proper nouns (names of people, cities, countries)
- Words the user specifically asks to exclude
- Any category the user mentions

Only return words that match the user's criteria. Return an empty list if nothing matches.
"""


class CleanedText(BaseModel):
    title: str
    cleaned_text: str  # German text with | delimiters


class TranslatedText(BaseModel):
    english_text: str  # English text with | delimiters


class VerifiedPair(BaseModel):
    german_text: str   # corrected German with | delimiters
    english_text: str  # corrected English with | delimiters


class ExcludedWords(BaseModel):
    words: list[str]  # words to exclude (case-insensitive matching)


class GeneratedTargetWord(BaseModel):
    index: int
    sentence_index: int
    word: str
    excluded: bool = False


class GeneratedLesson(BaseModel):
    title: str
    text_source: str
    target_data: list[GeneratedTargetWord]


def _build_target_data(
    german_chunks: list[str],
    excluded_words: set[str] | None = None,
) -> list[GeneratedTargetWord]:
    """Deterministically build target_data from German chunks."""
    excluded_lower = {w.lower() for w in (excluded_words or set())}
    words = []
    global_index = 0
    for sentence_idx, chunk in enumerate(german_chunks):
        for token in chunk.split():
            clean = re.sub(r"[.,;:!?\"'()…\-–—]", "", token).strip()
            if not clean:
                continue
            words.append(GeneratedTargetWord(
                index=global_index,
                sentence_index=sentence_idx,
                word=clean,
                excluded=clean.lower() in excluded_lower,
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

    # Step 3: Verify alignment and fix issues
    logger.info("Step 3: Verifying alignment...")
    verify_response = await client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": VERIFY_PROMPT},
            {"role": "user", "content": f"German:\n{cleaned.cleaned_text}\n\nEnglish:\n{translated.english_text}"},
        ],
        response_format=VerifiedPair,
    )
    verified = verify_response.choices[0].message.parsed
    german_final = verified.german_text
    english_final = verified.english_text
    logger.info("Step 3 done: DE chunks=%d, EN chunks=%d",
                german_final.count("|") + 1, english_final.count("|") + 1)

    # Step 4 (optional): Determine excluded words if user prompt suggests it
    excluded_words: set[str] = set()
    if prompt.strip():
        german_chunks = [c.strip() for c in german_final.split("|") if c.strip()]
        all_words = set()
        for chunk in german_chunks:
            for token in chunk.split():
                clean = re.sub(r"[.,;:!?\"'()…\-–—]", "", token).strip()
                if clean:
                    all_words.add(clean)

        logger.info("Step 4: Checking for excluded words...")
        exclude_response = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": EXCLUDE_PROMPT},
                {"role": "user", "content": f"Words: {', '.join(sorted(all_words))}\n\nUser instructions: {prompt}"},
            ],
            response_format=ExcludedWords,
        )
        excluded_words = set(exclude_response.choices[0].message.parsed.words)
        logger.info("Step 4 done: excluded=%s", excluded_words)

    # Build the lesson deterministically
    german_chunks = [c.strip() for c in german_final.split("|") if c.strip()]
    target_data = _build_target_data(german_chunks, excluded_words)

    return GeneratedLesson(
        title=cleaned.title,
        text_source=english_final,
        target_data=target_data,
    )
