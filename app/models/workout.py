import uuid
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.enums import SetType

if TYPE_CHECKING:
    from .user import User
    from .workout_program import WorkoutProgram
    from .routine import Routine, RoutineExercise
    from .exercise import Exercise


class WorkoutSession(SQLModel, table=True):
    __tablename__ = "workout_sessions"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    workout_program_id: Optional[uuid.UUID] = Field(default=None, foreign_key="workout_programs.id", nullable=True)
    routine_id: Optional[uuid.UUID] = Field(default=None, foreign_key="routines.id", nullable=True)

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    ended_at: Optional[datetime] = Field(default=None, nullable=True)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relaciones
    workout_program: Optional["WorkoutProgram"] = Relationship(back_populates="workout_sessions")
    routine: Optional["Routine"] = Relationship(back_populates="workout_sessions")

    # Series individuales (borrado en cascada)
    sets: List["WorkoutSet"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class WorkoutSet(SQLModel, table=True):
    __tablename__ = "workout_sets"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    session_id: uuid.UUID = Field(foreign_key="workout_sessions.id", index=True, nullable=False)
    routine_exercise_id: Optional[uuid.UUID] = Field(default=None, foreign_key="routine_exercises.id", nullable=True)
    exercise_id: uuid.UUID = Field(foreign_key="exercises.id", index=True, nullable=False)

    set_number: int = Field(nullable=False)
    set_type: SetType = Field(default=SetType.NORMAL, nullable=False)
    reps_done: int = Field(nullable=False)
    weight_kg: Optional[float] = Field(default=None, nullable=True)
    rir: Optional[int] = Field(default=None, nullable=True)
    rpe: Optional[float] = Field(default=None, nullable=True)
    completed: bool = Field(default=True, nullable=False)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relaciones
    session: WorkoutSession = Relationship(back_populates="sets")
    routine_exercise: Optional["RoutineExercise"] = Relationship(back_populates="workout_sets")
    exercise: "Exercise" = Relationship(back_populates="workout_sets")
