from uuid import UUID
from enum import StrEnum
import redis.asyncio as redis
from app.services.constants import TICKET_FORMAT


class TicketStatus(StrEnum):
    PENDING = "pending"
    MATCHED = "matched"


async def enqueue_player(client: redis.Redis, player_id: UUID):
    ticket_key = TICKET_FORMAT.format(str(player_id))

    await client.hset(
        ticket_key,
        mapping={"status": TicketStatus.PENDING, "match_id": str(UUID(int=0))},
    )
    await client.zadd("mm:queue", {str(player_id): 10})
    return ticket_key


async def get_ticket_status(client: redis.Redis, player_id: UUID):
    return await client.hgetall(TICKET_FORMAT.format(str(player_id)))
