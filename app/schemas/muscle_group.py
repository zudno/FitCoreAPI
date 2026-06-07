from uuid import UUID
from pydantic import BaseModel


class MuscleGroupBase(BaseModel):
    name: str


class MuscleGroupCreate(MuscleGroupBase):
    pass


class MuscleGroupRead(MuscleGroupBase):
    id: UUID

    class Config:
        from_attributes = True
