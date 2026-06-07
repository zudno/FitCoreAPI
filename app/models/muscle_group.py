import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .exercise import Exercise


class MuscleGroup(SQLModel, table=True):
    __tablename__ = "muscle_groups"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str = Field(unique=True, index=True, nullable=False)

    # Relación uno-a-muchos con Exercise
    exercises: List["Exercise"] = Relationship(back_populates="muscle_group")
