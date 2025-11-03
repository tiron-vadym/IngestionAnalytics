from arq.connections import create_pool, RedisSettings
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError

from app.db import AsyncSessionLocal
from app.models.events import Event

redis_settings = RedisSettings(host='redis', port=6379)


async def enqueue_events(events: list[dict]):
    redis = await create_pool(RedisSettings(host='redis', port=6379))
    try:
        for event in events:
            event_serializable = event.copy()
            if isinstance(event_serializable.get("event_id"), UUID):
                event_serializable["event_id"] = int(event_serializable["event_id"])
            if isinstance(event_serializable.get("occurred_at"), datetime):
                event_serializable["occurred_at"] = event_serializable["occurred_at"].isoformat()

            await redis.enqueue_job("process_event", event_serializable)
    finally:
        await redis.close()


async def process_event(ctx, event_data: dict):
    async with AsyncSessionLocal() as session:
        try:
            event = Event(
                event_id=UUID(int=event_data["event_id"]),
                occurred_at=datetime.fromisoformat(event_data["occurred_at"]),
                user_id=event_data["user_id"],
                event_type=event_data["event_type"],
                properties=event_data.get("properties", {})
            )
            session.add(event)
            await session.commit()
            print(f"[INFO] Event saved: {event.event_id}")
        except SQLAlchemyError as e:
            await session.rollback()
            await write_to_dead_letter(ctx, event_data, str(e))
            raise


async def write_to_dead_letter(ctx, event_data: dict, error_message: str):
    redis = ctx['redis']
    payload = {
        "failed_event": event_data,
        "error": error_message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await redis.rpush("dead_letter", str(payload))
    print(f"[DEAD-LETTER] {error_message} for event {event_data.get('event_id')}")


class WorkerSettings:
    functions = [process_event]
    redis_settings = redis_settings
    max_tries = 3
    retry_jobs = True
    job_timeout = 30
