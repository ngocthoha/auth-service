from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str
    exp: int
    role: str


class RefreshTokenCreate(BaseModel):
    token: str
    expires_at: int
    user_id: str 