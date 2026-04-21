from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import games, lessons, sidebar

app = FastAPI(title="MonkeyDo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sidebar.router)
app.include_router(lessons.router)
app.include_router(games.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
