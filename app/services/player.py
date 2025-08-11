from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Player
from app.exceptions import PlayerAlreadyExistsError, PlayerNotFoundError


async def create_player(username: str, db: Session):
    stmt = select(Player).where(Player.username == username)
    player_exists = (await db.scalars(statement=stmt)).first()

    if player_exists:
        raise PlayerAlreadyExistsError()

    player = Player(username=username)
    db.add(player)
    await db.commit()
    await db.refresh(player)
    return player


async def get_player(id: UUID, db: Session) -> Player:
    stmt = select(Player).where(Player.id == id)
    player = (await db.scalars(statement=stmt)).first()

    if not player:
        raise PlayerNotFoundError()

    return player
