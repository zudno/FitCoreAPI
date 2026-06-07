from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from ..models.enums import SetType
from .exercise import ExerciseRead


# ============================================================
# WORKOUT SET SCHEMAS
# ============================================================

class WorkoutSetBase(BaseModel):
    exercise_id: UUID
    set_number: int
    set_type: SetType = SetType.NORMAL
    reps_done: int
    weight_kg: Optional[float] = None
    rir: Optional[int] = None
    rpe: Optional[float] = None
    completed: bool = True
    notes: Optional[str] = None


class WorkoutSetCreate(WorkoutSetBase):
    routine_exercise_id: Optional[UUID] = None


class WorkoutSetUpdate(BaseModel):
    exercise_id: Optional[UUID] = None
    set_number: Optional[int] = None
    set_type: Optional[SetType] = None
    reps_done: Optional[int] = None
    weight_kg: Optional[float] = None
    rir: Optional[int] = None
    rpe: Optional[float] = None
    completed: Optional[bool] = None
    notes: Optional[str] = None
    routine_exercise_id: Optional[UUID] = None


class WorkoutSetRead(WorkoutSetBase):
    id: UUID
    session_id: UUID
    routine_exercise_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutSetDetail(WorkoutSetRead):
    exercise: ExerciseRead


# ============================================================
# WORKOUT SESSION SCHEMAS
# ============================================================

class WorkoutSessionBase(BaseModel):
    workout_program_id: Optional[UUID] = None
    routine_id: Optional[UUID] = None
    notes: Optional[str] = None


class WorkoutSessionCreate(WorkoutSessionBase):
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    sets: Optional[List[WorkoutSetCreate]] = None


class WorkoutSessionUpdate(BaseModel):
    ended_at: Optional[datetime] = None
    notes: Optional[str] = None


class WorkoutSessionRead(WorkoutSessionBase):
    id: UUID
    user_id: UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutSessionDetail(WorkoutSessionRead):
    sets: List[WorkoutSetDetail]
