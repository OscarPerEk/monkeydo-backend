from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import DEFAULT_USER_ID
from app.database import get_db
from app.models.folder import Folder
from app.models.lesson import Lesson
from app.schemas.sidebar import FolderOut, LessonSummary, SidebarResponse

router = APIRouter()


@router.get("/sidebar", response_model=SidebarResponse)
async def get_sidebar(db: AsyncSession = Depends(get_db)):
    # Active folders for the default user, with their lessons eager-loaded
    folder_result = await db.execute(
        select(Folder)
        .where(Folder.user_id == DEFAULT_USER_ID, Folder.deleted_at.is_(None))
        .order_by(Folder.created_at)
    )
    folders = folder_result.scalars().all()

    # Root-level lessons (no folder)
    root_result = await db.execute(
        select(Lesson).where(
            Lesson.user_id == DEFAULT_USER_ID,
            Lesson.folder_id.is_(None),
            Lesson.deleted_at.is_(None),
        )
    )
    root_lessons = root_result.scalars().all()

    folders_out = []
    for folder in folders:
        active_lessons = [l for l in folder.lessons if l.deleted_at is None]
        folders_out.append(
            FolderOut(
                id=folder.id,
                name=folder.name,
                lessons=[LessonSummary(id=l.id, title=l.title) for l in active_lessons],
            )
        )

    return SidebarResponse(
        folders=folders_out,
        root_lessons=[LessonSummary(id=l.id, title=l.title) for l in root_lessons],
    )
