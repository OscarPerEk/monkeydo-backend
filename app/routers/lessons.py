import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

from app.config import DEFAULT_USER_ID
from app.database import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import (
    CreateLessonRequest,
    GenerateRequest,
    GenerateResponse,
    LessonDetail,
    LessonRangeUpdate,
    TargetWord,
)
from app.services.generation import generate_lesson

router = APIRouter()


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
async def get_lesson(lesson_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id, Lesson.deleted_at.is_(None))
    )
    lesson = result.scalar_one_or_none()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        text_source=lesson.text_source,
        target_data=[TargetWord(**w) for w in lesson.target_data],
        range_start_index=lesson.range_start_index,
        range_end_index=lesson.range_end_index,
    )


@router.post("/lessons/generate", response_model=GenerateResponse)
async def generate(body: GenerateRequest):
    logger.info("POST /lessons/generate — text=%d chars, prompt=%d chars", len(body.german_text), len(body.prompt))
    try:
        logger.info("Calling OpenAI...")
        result = await generate_lesson(body.german_text, body.prompt)
        logger.info("OpenAI returned: title=%s, words=%d", result.title, len(result.target_data))
    except Exception as e:
        logger.exception("LLM generation failed")
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {e}")

    return GenerateResponse(
        title=result.title,
        text_source=result.text_source,
        target_data=[TargetWord(**w.model_dump()) for w in result.target_data],
    )


@router.post("/lessons", response_model=LessonDetail)
async def create_lesson(body: CreateLessonRequest, db: AsyncSession = Depends(get_db)):
    logger.info("POST /lessons — title=%s", body.title)
    lesson = Lesson(
        user_id=DEFAULT_USER_ID,
        folder_id=body.folder_id,
        title=body.title,
        text_source=body.text_source,
        target_data=[w.model_dump() for w in body.target_data],
    )
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)

    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        text_source=lesson.text_source,
        target_data=[TargetWord(**w) for w in lesson.target_data],
        range_start_index=lesson.range_start_index,
        range_end_index=lesson.range_end_index,
    )


@router.patch("/lessons/{lesson_id}/range", response_model=LessonDetail)
async def update_range(
    lesson_id: uuid.UUID, body: LessonRangeUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    lesson.range_start_index = body.start_index
    lesson.range_end_index = body.end_index
    await db.commit()
    await db.refresh(lesson)
    return lesson
