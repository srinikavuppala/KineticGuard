from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.consent import ConsentResponse
from app.models.consent import Consent
from app.core.security import oauth2_scheme, decode_token
from sqlalchemy import select

router = APIRouter(prefix="/consents", tags=["Consent & Legal"])


@router.post("/accept", response_model=ConsentResponse, status_code=status.HTTP_201_CREATED)
async def accept_disclaimer(
        request: Request,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    # 1. Unpack the VIP badge to see who is signing
    payload = decode_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 2. Create the legal paper trail
    new_consent = Consent(
        user_id=user_id,
        ip_address=request.client.host,  # Logs their IP address
        user_agent=request.headers.get("user-agent", "Unknown")  # Logs their phone/browser
    )

    db.add(new_consent)
    await db.flush()

    return new_consent