import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # Free-text string to accept any Android gesture (THUMB_DOWN, INDEX_UP, etc.)
    trigger_method = Column(String(50), nullable=False)
    model_version = Column(String(50), nullable=True)

    gesture_profile = Column(String(50), nullable=False, default="DEFAULT", server_default="DEFAULT")
    status = Column(String(50), default="ACTIVE", server_default="ACTIVE")

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_accuracy = Column(Float, nullable=True)
    location_method = Column(String(50), nullable=True)
    location_address = Column(Text, nullable=True)

    resolution_notes = Column(Text, nullable=True)
    resolved_by = Column(UUID(as_uuid=True), nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    expired_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "gesture_profile IN ('DEFAULT', 'HEALTHCARE', 'TEACHER', 'DELIVERY', 'CORPORATE', 'ELDERLY')",
            name="ck_alerts_profile_valid"
        ),
        CheckConstraint(
            "status IN ('ACTIVE', 'RESOLVED', 'EXPIRED')",
            name="ck_alerts_status_valid"
        ),
    )