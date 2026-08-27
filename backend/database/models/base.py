"""
SQLAlchemy Base Model with UUID Primary Keys, Timestamping, and Audit Mixins
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Text
from backend.database.session import Base


class TimeStampedUUIDModel(Base):
    """Abstract base model adding UUID v4 primary keys and automatic UTC timestamping."""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)
