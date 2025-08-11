from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions import GameError
from app.routes import matches, matchmaking, players, root
from app.workers.matchmaker import match_players


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        match_players,
        trigger=IntervalTrigger(seconds=3),
        id="matchmaker",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

scheduler = AsyncIOScheduler()

app.include_router(players.router)
app.include_router(matches.router)
app.include_router(matchmaking.router)
app.include_router(root.router)


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.exception_handler(GameError)
async def game_exception_handler(_, error: GameError):
    raise HTTPException(status_code=error.status_code, detail=error.detail)


@app.exception_handler(Exception)
async def default_exception_handler(_, error):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
