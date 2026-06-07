from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from ..models.enums import RoutineGoal, RoutineLevel
from .routine import RoutineCreate, RoutineDetail


# ============================================================
# WORKOUT PROGRAM SCHEMAS
# ============================================================

class WorkoutProgramBase(BaseModel):
    name: str
    goal: Optional[RoutineGoal] = None
    level: Optional[RoutineLevel] = None
    is_active: bool = False
    description: Optional[str] = None
    image_url: Optional[str] = None


class WorkoutProgramCreate(WorkoutProgramBase):
    routines: Optional[List[RoutineCreate]] = None


class WorkoutProgramUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[RoutineGoal] = None
    level: Optional[RoutineLevel] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    routines: Optional[List[RoutineCreate]] = None


class WorkoutProgramRead(WorkoutProgramBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class WorkoutProgramDetail(WorkoutProgramRead):
    routines: List[RoutineDetail]

    class Config:
        from_attributes = True
