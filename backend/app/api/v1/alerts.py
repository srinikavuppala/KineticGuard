from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.alert import CreateAlertRequest, AlertResponse, UpdateAlertStatusRequest
from app.services import alert_service

# IMPORTS FOR AUTHENTICATION
from app.core.security import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(tags=["Alerts"])


# ==========================================
# 1. WEBSOCKET MANAGER (NEW)
# ==========================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass  # Connection was closed by client


ws_manager = ConnectionManager()


# ==========================================
# 2. WEBSOCKET ENDPOINT (NEW)
# ==========================================
@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Just keep the connection alive waiting for pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# ==========================================
# 3. MOBILE APP: Trigger SOS
# ==========================================
@router.post("/alerts/trigger", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def trigger_sos_route(
        request: CreateAlertRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        alert = await alert_service.create_alert(db, user_id=current_user.id, request=request)

        # BROADCAST TO ALL CONNECTED DASHBOARDS (NEW)
        alert_dict = {
            "id": str(alert.id),
            "user_id": str(alert.user_id),
            "trigger_method": alert.trigger_method,
            "gesture_profile": alert.gesture_profile,
            "model_version": alert.model_version,
            "status": alert.status,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "location_address": alert.location_address,
            "created_at": alert.created_at.isoformat() if alert.created_at else None
        }
        await ws_manager.broadcast(alert_dict)

        return alert
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 4. REACT DASHBOARD: Get list of alerts
# ==========================================
@router.get("/alerts", response_model=list[AlertResponse])
async def list_all_alerts(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await alert_service.get_all_alerts(db)


# ==========================================
# 5. SWAGGER: Get single alert
# ==========================================
@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: UUID, db: AsyncSession = Depends(get_db)):
    alert = await alert_service.get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


# ==========================================
# 6. ADMIN: Resolve alert
# ==========================================
@router.put("/alerts/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
        alert_id: UUID,
        request: UpdateAlertStatusRequest,
        db: AsyncSession = Depends(get_db)
):
    test_admin_id = UUID("00000000-0000-0000-0000-000000000002")
    try:
        alert = await alert_service.resolve_alert(db, alert_id, test_admin_id, request)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))