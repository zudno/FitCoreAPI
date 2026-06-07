import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING

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
    avatar_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relación con Profile
    profile: Optional["Profile"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})
