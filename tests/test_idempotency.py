from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.events import Event
from app.workers.events_worker import enqueue_events


def test_bulk_insert_idempotent(db: Session):
    event_id = uuid4()
    events = [
        {
            "event_id": event_id,
            "occurred_at": "2025-10-30T12:00:00",
            "user_id": 1,
            "event_type": "login",
            "properties": None
        }
    ]

    inserted_1 = enqueue_events(events)
    inserted_2 = enqueue_events(events)

    assert inserted_1 == 1
    assert inserted_2 == 0

    assert db.query(Event).filter(Event.event_id == event_id).count() == 1
