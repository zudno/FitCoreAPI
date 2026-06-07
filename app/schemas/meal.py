import uuid
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class IngredientSchema(BaseModel):
    name: str = Field(..., description="Nombre del ingrediente")
    estimated_weight_g: float = Field(..., description="Peso estimado en gramos")
    calories: float = Field(..., description="Calorías en kcal")
    protein_g: float = Field(..., description="Proteínas en gramos")
    carbs_g: float = Field(..., description="Carbohidratos en gramos")
    fat_g: float = Field(..., description="Grasas en gramos")


class MealAnalysisResponse(BaseModel):
    success: bool = Field(..., description="Indica si el análisis fue exitoso")
    error: str | None = Field(None, description="Mensaje de error si success es False")
    food_name: str = Field(..., description="Nombre del platillo identificado")
    estimated_total_weight_g: float = Field(..., description="Peso total estimado en gramos")
    total_calories: float = Field(..., description="Calorías totales en kcal")
    total_protein_g: float = Field(..., description="Proteínas totales en gramos")
    total_carbs_g: float = Field(..., description="Carbohidratos totales en gramos")
    total_fat_g: float = Field(..., description="Grasas totales en gramos")
    ingredients: list[IngredientSchema] = Field(
        default_factory=list,
        description="Desglose por ingrediente",
    )
    image_url: str | None = Field(None, description="URL pública de la imagen procesada")

    model_config = {"from_attributes": True}


class MealCreate(BaseModel):
    name: str
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    ingredients: list[IngredientSchema] = []
    image_url: str | None = None


class MealRead(MealCreate):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        if dt.tzinfo is None:
            return dt.isoformat() + "Z"
        return dt.isoformat().replace("+00:00", "Z")

    model_config = {"from_attributes": True}


class DailyNutritionTargets(BaseModel):
    daily_calories: int
    daily_protein_g: int
    daily_carbs_g: int
    daily_fat_g: int
