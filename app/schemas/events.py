from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EventRequest(BaseModel):
    event_id: UUID
    occurred_at: datetime
    user_id: int
    event_type: str
    properties: dict | None = None
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }
