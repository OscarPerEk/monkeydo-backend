from uuid import UUID

from pydantic import BaseModel


class TargetWord(BaseModel):
    index: int
    sentence_index: int
    word: str
    excluded: bool = False


class LessonDetail(BaseModel):
    id: UUID
    title: str
    text_source: str
    target_data: list[TargetWord]
    range_start_index: int | None = None
    range_end_index: int | None = None

    model_config = {"from_attributes": True}


class GenerateRequest(BaseModel):
    german_text: str
    prompt: str = ""


class GenerateResponse(BaseModel):
    title: str
    text_source: str
    target_data: list[TargetWord]


class LessonRangeUpdate(BaseModel):
    start_index: int | None = None
    end_index: int | None = None


class CreateLessonRequest(BaseModel):
    title: str
    text_source: str
    target_data: list[TargetWord]
    folder_id: UUID | None = None
