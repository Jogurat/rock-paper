import json
from uuid import UUID

import redis.asyncio as redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.choice import Choice, win_conditions
from app.database.models import Match, Player, PlayerMatch
from app.exceptions import (
    MatchAlreadyCompletedError,
    MatchNotFoundError,
    PlayerNotFoundError,
)
from app.services.constants import LEADERBOARD_KEY, MAX_MATCHES


async def get_match(match_id: UUID, db: AsyncSession) -> Match:
    stmt = select(Match).where(Match.id == match_id)
    match = (await db.scalars(statement=stmt)).first()
    if not match:
        raise MatchNotFoundError()
    return match


async def create_match(db: AsyncSession) -> Match:
    match = Match()
    db.add(match)
    await db.commit()
    await db.refresh(match)
    return match


async def play_move(
    *,
    match_id: UUID,
    player_id: UUID,
    choice: Choice,
    db: AsyncSession,
    redis: redis.Redis,
) -> Match:
    match_stmt = (
        select(Match)
        .options(selectinload(Match.player_matches))
        .options(selectinload(Match.players))
        .where(Match.id == match_id)
    )
    player_stmt = select(Player).where(Player.id == player_id)

    match = (await db.scalars(statement=match_stmt)).first()
    if not match:
        raise MatchNotFoundError()
    if match.completed:
        raise MatchAlreadyCompletedError()

    player = (await db.scalars(statement=player_stmt)).first()
    if not player:
        raise PlayerNotFoundError()

    match.add_player(player=player, move=choice)

    is_last_move = len(match.player_matches) == 2

    if is_last_move:
        first_move = match.player_matches[0]
        second_move = match.player_matches[1]
        winner = determine_winner(first_move, second_move)
        match.winner = winner.player if winner else None
        match.completed = True

    db.add(match)
    await db.commit()
    await db.refresh(match)

    if is_last_move:
        await redis.lpush(
            LEADERBOARD_KEY,
            json.dumps({"match_id": str(match.id), "winner_id": str(match.winner_id)}),
        )
        await redis.ltrim(LEADERBOARD_KEY, 0, MAX_MATCHES - 1)

    return match


async def get_leaderboard(redis: redis.Redis):
    matches = await redis.lrange(LEADERBOARD_KEY, 0, -1)
    return [json.loads(match) for match in matches]


async def clear_leaderboard(redis: redis.Redis):
    await redis.delete(LEADERBOARD_KEY)


def determine_winner(first_move: PlayerMatch, second_move: PlayerMatch):
    first_choice = first_move.move
    second_choice = second_move.move
    is_draw = first_choice == second_choice

    if is_draw:
        return None

    if second_choice in win_conditions[first_choice]:
        return first_move
    else:
        return second_move
