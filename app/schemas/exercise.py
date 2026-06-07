from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from .muscle_group import MuscleGroupRead


class ExerciseBase(BaseModel):
    muscle_group_id: UUID
    name: str
    equipment: Optional[str] = None
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    instructions: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    muscle_group_id: Optional[UUID] = None
    name: Optional[str] = None
    equipment: Optional[str] = None
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    instructions: Optional[str] = None


class ExerciseRead(ExerciseBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseDetail(ExerciseRead):
    muscle_group: MuscleGroupRead
