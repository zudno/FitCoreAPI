import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.enums import RoutineGoal, RoutineLevel

if TYPE_CHECKING:
    from .routine import Routine
    from .workout import WorkoutSession


class WorkoutProgram(SQLModel, table=True):
    __tablename__ = "workout_programs"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    name: str = Field(nullable=False)
    goal: Optional[RoutineGoal] = Field(default=None, nullable=True)
    level: Optional[RoutineLevel] = Field(default=None, nullable=True)
    is_active: bool = Field(default=False, nullable=False)
    image_url: Optional[str] = Field(default=None, nullable=True)
    description: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relaciones
    routines: List["Routine"] = Relationship(
        back_populates="program",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    workout_sessions: List["WorkoutSession"] = Relationship(back_populates="workout_program")
