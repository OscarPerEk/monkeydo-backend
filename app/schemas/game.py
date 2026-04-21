from uuid import UUID

from pydantic import BaseModel


class GameStartRequest(BaseModel):
    lesson_id: UUID
    duration_seconds: int
    difficulty: str


class GameStartResponse(BaseModel):
    session_id: UUID


class WordHistoryEntry(BaseModel):
    word_index: int
    typed_word: str
    status: str
    attempts: int
    latency_ms: int


class GameFinishRequest(BaseModel):
    session_id: UUID
    word_history: list[WordHistoryEntry]


class GameFinishResponse(BaseModel):
    ok: bool
