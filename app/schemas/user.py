from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import AuthProvider


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    auth_provider: AuthProvider
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    has_profile: bool = False
