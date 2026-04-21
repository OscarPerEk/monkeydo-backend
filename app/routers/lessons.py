import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.lesson import Lesson
from app.schemas.lesson import LessonDetail, TargetWord

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
    )
