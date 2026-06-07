import uuid
from datetime import date, datetime, timezone
from typing import Optional, TYPE_CHECKING
from .enums import Gender, ActivityLevel, FitnessGoal, UnitSystem

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", unique=True, index=True, nullable=False)
    
    gender: Gender = Field(nullable=False)
    date_of_birth: date = Field(nullable=False)
    height: float = Field(nullable=False)  # En cm
    weight: float = Field(nullable=False)  # En kg
    activity_level: ActivityLevel = Field(nullable=False)
    goal: FitnessGoal = Field(nullable=False)
    unit_system: UnitSystem = Field(default=UnitSystem.METRIC, nullable=False)
    
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relación con User
    user: "User" = Relationship(back_populates="profile")
