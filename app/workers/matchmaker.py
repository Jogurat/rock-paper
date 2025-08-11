import logging

from app.database.database import AsyncSessionLocal
from app.database.models import Match
from app.dependencies import get_redis
from app.services.constants import QUEUE_KEY, TICKET_FORMAT
from app.services.matchmaking import TicketStatus

logger = logging.getLogger("uvicorn")

redis = get_redis()


async def match_players():
    queue = await redis.zrangebyscore(QUEUE_KEY, 0, 100)
    matched = queue[0:2]

    if len(matched) != 2:
        return

    async with AsyncSessionLocal() as session:
        logger.info("Matching players...")
        match = Match()
        session.add(match)
        await session.commit()
        await session.refresh(match)

        await redis.hset(
            TICKET_FORMAT.format(matched[0]),
            mapping={"match_id": str(match.id), "status": TicketStatus.MATCHED},
        )
        await redis.hexpire(TICKET_FORMAT.format(matched[0]), 15, "match_id", "status")

        await redis.hset(
            TICKET_FORMAT.format(matched[1]),
            mapping={"match_id": str(match.id), "status": TicketStatus.MATCHED},
        )
        await redis.hexpire(TICKET_FORMAT.format(matched[1]), 15, "match_id", "status")

        await redis.zrem(QUEUE_KEY, matched[0])
        await redis.zrem(QUEUE_KEY, matched[1])
