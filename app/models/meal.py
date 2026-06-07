import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Meal(SQLModel, table=True):
    __tablename__ = "meals"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)
    
    name: str = Field(nullable=False)
    calories: float = Field(nullable=False)
    protein_g: float = Field(nullable=False)
    carbs_g: float = Field(nullable=False)
    fat_g: float = Field(nullable=False)
    
    # Guardamos los ingredientes como un JSON para flexibilidad
    ingredients: List[dict] = Field(default_factory=list, sa_column=Column(JSON))
    
    image_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True
    )
