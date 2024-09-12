from pydantic import BaseModel
from datetime import datetime


class TokenData(BaseModel):
    expires: int = 30
    id: str


class TokenExpiry(BaseModel):
    expiry: datetime
