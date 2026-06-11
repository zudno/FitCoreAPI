from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models.enums import AuthProvider

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    auth_provider: AuthProvider
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
