import httpx
from app.config import get_settings

settings = get_settings()


async def get_address_from_coords(latitude: float, longitude: float) -> str | None:
    """Converts GPS coordinates to a readable address using OpenStreetMap (Nominatim)"""
    if not latitude or not longitude:
        return None

    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "extratags": 1
    }

    # Nominatim requires a custom User-Agent
    headers = {
        "User-Agent": settings.NOMINATIM_USER_AGENT
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            return data.get("display_name", "Unknown Location")
    except Exception:
        return "Address lookup failed"