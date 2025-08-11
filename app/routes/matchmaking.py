from fastapi import APIRouter, Depends
from uuid import UUID
from app.dependencies import get_redis
from app.services.matchmaking import (
    get_ticket_status as get_status,
    enqueue_player,
    TicketStatus,
)
import redis.asyncio as redis
from pydantic import BaseModel

router = APIRouter(prefix="/matchmaking", tags=["matchmaking"])


class EnqeueRequest(BaseModel):
    player_id: UUID


class EnqueueResponse(BaseModel):
    ticket_id: str


@router.post("/", response_model=EnqueueResponse)
async def enqueue(request: EnqeueRequest, client: redis.Redis = Depends(get_redis)):
    ticket_id = await enqueue_player(client=client, player_id=request.player_id)
    return {"ticket_id": ticket_id}


class TicketStatusResponse(BaseModel):
    status: TicketStatus
    match_id: UUID


@router.get("/status/{player_id}")
async def get_ticket_status(player_id: UUID, client: redis.Redis = Depends(get_redis)):
    return await get_status(client=client, player_id=player_id)
