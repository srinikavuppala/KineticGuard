from pydantic import BaseModel

class LoginRequest(BaseModel):
    """Data sent by the user to log in"""
    email: str
    password: str

class Token(BaseModel):
    """The VIP badge handed to the user"""
    access_token: str
    token_type: str = "bearer"