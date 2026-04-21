from uuid import UUID

from pydantic import BaseModel


class LessonSummary(BaseModel):
    id: UUID
    title: str

    model_config = {"from_attributes": True}


class FolderOut(BaseModel):
    id: UUID
    name: str
    lessons: list[LessonSummary]

    model_config = {"from_attributes": True}


class SidebarResponse(BaseModel):
    folders: list[FolderOut]
    root_lessons: list[LessonSummary]
