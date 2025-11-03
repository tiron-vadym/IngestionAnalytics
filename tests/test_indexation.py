from uuid import uuid4
from sqlalchemy.orm import Session

from app.models.events import Event


def test_event_indexes(db: Session):
    events = [
        Event(
            event_id=uuid4(),
            occurred_at="2025-10-30T12:00:00",
            user_id=1,
            event_type="login"
        ),
        Event(
            event_id=uuid4(),
            occurred_at="2025-10-30T13:00:00",
            user_id=2,
            event_type="purchase"
        ),
    ]
    db.add_all(events)
    db.commit()

    login_events = db.query(Event).filter(Event.user_id == 1).all()
    assert len(login_events) == 1
    assert login_events[0].event_type == "login"

    purchase_events = db.query(Event).filter(Event.event_type == "purchase").all()
    assert len(purchase_events) == 1
