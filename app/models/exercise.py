import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .muscle_group import MuscleGroup
    from .routine import RoutineExercise
    from .workout import WorkoutSet


class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    muscle_group_id: uuid.UUID = Field(foreign_key="muscle_groups.id", index=True, nullable=False)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True, nullable=True)
    
    name: str = Field(nullable=False)
    equipment: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    gif_url: Optional[str] = Field(default=None)
    instructions: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relaciones
    muscle_group: "MuscleGroup" = Relationship(back_populates="exercises")
    routine_exercises: List["RoutineExercise"] = Relationship(back_populates="exercise")
    workout_sets: List["WorkoutSet"] = Relationship(back_populates="exercise")
