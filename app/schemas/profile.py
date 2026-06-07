from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from ..models.enums import Gender, ActivityLevel, FitnessGoal, UnitSystem


class ProfileBase(BaseModel):
    gender: Gender
    date_of_birth: date
    height: float
    weight: float
    activity_level: ActivityLevel
    goal: FitnessGoal
    unit_system: UnitSystem = UnitSystem.METRIC


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    goal: Optional[FitnessGoal] = None
    unit_system: Optional[UnitSystem] = None


class ProfileRead(ProfileBase):
    id: UUID
    user_id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True
