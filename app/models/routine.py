import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, JSON, UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship
from app.models.enums import UnitSystem
from app.models.workout_program import WorkoutProgram

if TYPE_CHECKING:
    from .user import User
    from .exercise import Exercise
    from .workout import WorkoutSession, WorkoutSet


class Routine(SQLModel, table=True):
    __tablename__ = "routines"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    program_id: uuid.UUID = Field(foreign_key="workout_programs.id", index=True, nullable=False)
    day_numbers: List[int] = Field(default_factory=list, sa_column=Column(JSON))
    label: Optional[str] = Field(default=None, nullable=True)
    muscle_focus: Optional[str] = Field(default=None, nullable=True)

    # Relaciones
    program: WorkoutProgram = Relationship(back_populates="routines")
    exercises: List["RoutineExercise"] = Relationship(
        back_populates="routine",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    workout_sessions: List["WorkoutSession"] = Relationship(back_populates="routine")


class RoutineExercise(SQLModel, table=True):
    __tablename__ = "routine_exercises"
    __table_args__ = (
        UniqueConstraint("routine_id", "position", name="uq_routine_position"),
    )

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    routine_id: uuid.UUID = Field(foreign_key="routines.id", index=True, nullable=False)
    exercise_id: uuid.UUID = Field(foreign_key="exercises.id", index=True, nullable=False)

    position: int = Field(default=1, nullable=False)
    rest_seconds: int = Field(default=90, nullable=False)
    weight_unit: UnitSystem = Field(default=UnitSystem.METRIC, nullable=False)
    notes: Optional[str] = Field(default=None)
    sets_config: Optional[List[dict]] = Field(default_factory=list, sa_column=Column(JSON))

    # Relaciones
    routine: Routine = Relationship(back_populates="exercises")
    exercise: "Exercise" = Relationship(back_populates="routine_exercises")
    workout_sets: List["WorkoutSet"] = Relationship(back_populates="routine_exercise")
