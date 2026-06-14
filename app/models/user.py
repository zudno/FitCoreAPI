import uuid
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

from app.models.enums import AuthProvider

if TYPE_CHECKING:
    from .profile import Profile


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    auth_provider: AuthProvider = Field(
        default=AuthProvider.NATIVE,
        sa_column=sa.Column(
            sa.Enum(AuthProvider, name="authprovider"),
            nullable=False,
            server_default=AuthProvider.NATIVE.value,
        ),
    )
    avatar_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relación con Profile
    profile: Optional["Profile"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

    @property
    def has_profile(self) -> bool:
        return self.profile is not None
