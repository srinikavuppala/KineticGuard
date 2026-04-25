from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.alert import Alert
from app.schemas.alert import AlertStatus
from app.schemas.alert import CreateAlertRequest, UpdateAlertStatusRequest
from datetime import datetime, timezone

# 1. Import Celery task
from app.tasks.notification_tasks import process_sos_alert_task
# 2. NEW: Import the Geocoding function
from app.utils.geocoding import get_address_from_coords


async def create_alert(db: AsyncSession, user_id: UUID, request: CreateAlertRequest) -> Alert:
    new_alert = Alert(
        user_id=user_id,
        trigger_method=request.trigger_method,             # REMOVED .value (it's a string now)
        gesture_profile=request.gesture_profile.value,     # Keep .value (still an Enum)
        model_version=request.model_version,
        latitude=request.latitude,
        longitude=request.longitude,
        location_accuracy=request.location_accuracy,
        location_method=request.location_method,
        status="ACTIVE"                                    # Changed to string
    )

    # 3. Fetch real address from OpenStreetMap before saving
    if request.latitude and request.longitude:
        new_alert.location_address = await get_address_from_coords(
            latitude=request.latitude,
            longitude=request.longitude
        )

    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)

    # Format timestamp for the email
    time_str = new_alert.created_at.strftime("%Y-%m-%d %H:%M:%S UTC") if new_alert.created_at else "Just now"

    # Hand off to Celery background worker
    process_sos_alert_task.delay(
        alert_id=str(new_alert.id),
        trigger_method=request.trigger_method,
        time_str=time_str
    )

    return new_alert


async def get_alert_by_id(db: AsyncSession, alert_id: UUID) -> Alert | None:
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    return result.scalar_one_or_none()


async def resolve_alert(db: AsyncSession, alert_id: UUID, admin_id: UUID,
                        request: UpdateAlertStatusRequest) -> Alert | None:
    alert = await get_alert_by_id(db, alert_id)
    if not alert:
        return None

    if alert.status != "ACTIVE":
        raise ValueError("Only ACTIVE alerts can be resolved.")

    alert.status = request.status.value
    alert.resolution_notes = request.resolution_notes
    alert.resolved_by = admin_id
    alert.resolved_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(alert)
    return alert


async def get_all_alerts(db: AsyncSession, limit: int = 50) -> list[Alert]:
    """Fetches the most recent alerts for the dashboard"""
    result = await db.execute(
        select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())