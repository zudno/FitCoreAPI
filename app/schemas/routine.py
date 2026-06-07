from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from ..models.enums import SetType, UnitSystem
from .exercise import ExerciseRead


# ============================================================
# SET CONFIG SCHEMA
# ============================================================

class SetConfigItem(BaseModel):
    set_number: int
    reps_min: int
    reps_max: int
    weight_kg: Optional[float] = None
    set_type: SetType = SetType.NORMAL


# ============================================================
# ROUTINE EXERCISE SCHEMAS
# ============================================================

class RoutineExerciseBase(BaseModel):
    exercise_id: UUID
    position: int = 1
    rest_seconds: int = 90
    weight_unit: UnitSystem = UnitSystem.METRIC
    notes: Optional[str] = None
    sets_config: Optional[List[SetConfigItem]] = None


class RoutineExerciseCreate(RoutineExerciseBase):
    pass


class RoutineExerciseUpdate(BaseModel):
    exercise_id: Optional[UUID] = None
    position: Optional[int] = None
    rest_seconds: Optional[int] = None
    weight_unit: Optional[UnitSystem] = None
    notes: Optional[str] = None
    sets_config: Optional[List[SetConfigItem]] = None


class RoutineExerciseRead(RoutineExerciseBase):
    id: UUID
    routine_id: UUID

    class Config:
        from_attributes = True


class RoutineExerciseDetail(RoutineExerciseRead):
    exercise: ExerciseRead


# ============================================================
# ROUTINE SCHEMAS
# ============================================================

class RoutineBase(BaseModel):
    day_numbers: List[int]
    label: Optional[str] = None
    muscle_focus: Optional[str] = None


class RoutineCreate(RoutineBase):
    exercises: Optional[List[RoutineExerciseCreate]] = None


class RoutineUpdate(BaseModel):
    day_numbers: Optional[List[int]] = None
    label: Optional[str] = None
    muscle_focus: Optional[str] = None
    exercises: Optional[List[RoutineExerciseCreate]] = None


class RoutineRead(RoutineBase):
    id: UUID
    program_id: UUID

    class Config:
        from_attributes = True


class RoutineDetail(RoutineRead):
    exercises: List[RoutineExerciseDetail]

    class Config:
        from_attributes = True
