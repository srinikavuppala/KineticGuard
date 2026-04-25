import uuid
from pydantic import BaseModel


class ConsentResponse(BaseModel):
    """The digital receipt given to the user after signing"""
    id: uuid.UUID
    user_id: uuid.UUID
    disclaimer_version: str

    class Config:
        from_attributes = True