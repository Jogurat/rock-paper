from uuid import UUID

import redis.asyncio as redis
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.choice import Choice
from app.dependencies import get_db, get_redis
from app.services import match


router = APIRouter(prefix="/matches", tags=["matches"])


class LeaderboardItem(BaseModel):
    match_id: UUID
    winner_id: UUID


@router.get("/leaderboard", response_model=list[LeaderboardItem])
async def get_current_leaderboard(redis: redis.Redis = Depends(get_redis)):
    return await match.get_leaderboard(redis)


@router.delete("/leaderboard")
async def clear_current_leaderboard(redis: redis.Redis = Depends(get_redis)):
    await match.clear_leaderboard(redis)
    return {"success": True}


@router.get("/{match_id}")
async def get_match_by_id(match_id: UUID, db: Session = Depends(get_db)):
    return await match.get_match(match_id, db)


@router.post("/")
async def create_match(db: Session = Depends(get_db)):
    return await match.create_match(db)


class PlayMove(BaseModel):
    player_id: UUID
    move: Choice


class PlayMoveResponse(BaseModel):
    completed: bool
    winner_id: UUID | None


@router.post("/{match_id}", response_model=PlayMoveResponse)
async def play_move(
    match_id: UUID,
    player_move: PlayMove,
    db: Session = Depends(get_db),
    redis: redis.Redis = Depends(get_redis),
):
    move = player_move.move
    return await match.play_move(
        match_id=match_id,
        choice=move,
        player_id=player_move.player_id,
        db=db,
        redis=redis,
    )
