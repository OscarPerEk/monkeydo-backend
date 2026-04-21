from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import DEFAULT_USER_ID
from app.database import get_db
from app.models.game_session import GameSession
from app.models.word_history import WordHistory
from app.schemas.game import (
    GameFinishRequest,
    GameFinishResponse,
    GameStartRequest,
    GameStartResponse,
)

router = APIRouter()


@router.post("/games/start", response_model=GameStartResponse)
async def start_game(request: GameStartRequest, db: AsyncSession = Depends(get_db)):
    session = GameSession(
        lesson_id=request.lesson_id,
        user_id=DEFAULT_USER_ID,
        difficulty=request.difficulty,
        duration_seconds=request.duration_seconds,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return GameStartResponse(session_id=session.id)


@router.post("/games/finish", response_model=GameFinishResponse)
async def finish_game(request: GameFinishRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GameSession).where(GameSession.id == request.session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    history_rows = [
        WordHistory(
            session_id=request.session_id,
            word_index=entry.word_index,
            typed_word=entry.typed_word,
            status=entry.status,
            attempts=entry.attempts,
            latency_ms=entry.latency_ms,
        )
        for entry in request.word_history
    ]
    db.add_all(history_rows)
    await db.commit()

    return GameFinishResponse(ok=True)
