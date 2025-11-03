from sqlalchemy import Column, Integer, Text, text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from uuid import uuid4
from sqlalchemy.orm import relationship

from app.db import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_type = Column(Text, nullable=False, index=True)
    properties = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("now()"))

    user = relationship("User", back_populates="events")
