from uuid import UUID

from pydantic import BaseModel


class TargetWord(BaseModel):
    index: int
    sentence_index: int
    source_word_index: int
    word: str


class LessonDetail(BaseModel):
    id: UUID
    title: str
    text_source: str
    target_data: list[TargetWord]

    model_config = {"from_attributes": True}
