import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


class TriggerMethod(str, Enum):
    GESTURE = "GESTURE"
    SHAKE = "SHAKE"
    POWER_BUTTON = "POWER_BUTTON"
    TIMEOUT = "TIMEOUT"
    MANUAL = "MANUAL"


class AlertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"
    EXPIRED = "EXPIRED"


class GestureProfile(str, Enum):
    DEFAULT = "DEFAULT"
    HEALTHCARE = "HEALTHCARE"
    TEACHER = "TEACHER"
    DELIVERY = "DELIVERY"
    CORPORATE = "CORPORATE"
    ELDERLY = "ELDERLY"


class CreateAlertRequest(BaseModel):
    # Changed to str to accept Android app gestures like "THUMB_DOWN"
    trigger_method: str = "GESTURE"
    gesture_profile: GestureProfile = GestureProfile.DEFAULT
    model_version: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_accuracy: float | None = None
    location_method: str = "UNKNOWN"
    notes: str | None = None

    model_config = ConfigDict(protected_namespaces=())


class AlertResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    trigger_method: str | None = None
    gesture_profile: str | None = None
    model_version: str | None = None
    status: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    location_address: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateAlertStatusRequest(BaseModel):
    status: AlertStatus
    resolution_notes: str | None = None