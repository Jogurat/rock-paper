from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.player import get_player, create_player as create_player_db
from pydantic import BaseModel

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/{player_id}")
async def get_player_by_id(player_id: UUID, db: Session = Depends(get_db)):
    return await get_player(player_id, db)


class CreatePlayerRequest(BaseModel):
    username: str


class CreatePlayerResponse(BaseModel):
    username: str
    id: UUID


@router.post("/")
async def create_player(request: CreatePlayerRequest, db: Session = Depends(get_db)):
    return await create_player_db(username=request.username, db=db)
