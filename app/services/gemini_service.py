import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.meal import MealAnalysisResponse


_RESPONSE_SCHEMA = genai.types.Schema(
    type=genai.types.Type.OBJECT,
    required=[
        "success",
        "food_name",
        "estimated_total_weight_g",
        "total_calories",
        "total_protein_g",
        "total_carbs_g",
        "total_fat_g",
        "ingredients",
    ],
    properties={
        "success": genai.types.Schema(type=genai.types.Type.BOOLEAN),
        "error": genai.types.Schema(type=genai.types.Type.STRING, nullable=True),
        "food_name": genai.types.Schema(type=genai.types.Type.STRING),
        "estimated_total_weight_g": genai.types.Schema(type=genai.types.Type.NUMBER),
        "total_calories": genai.types.Schema(type=genai.types.Type.NUMBER),
        "total_protein_g": genai.types.Schema(type=genai.types.Type.NUMBER),
        "total_carbs_g": genai.types.Schema(type=genai.types.Type.NUMBER),
        "total_fat_g": genai.types.Schema(type=genai.types.Type.NUMBER),
        "ingredients": genai.types.Schema(
            type=genai.types.Type.ARRAY,
            items=genai.types.Schema(
                type=genai.types.Type.OBJECT,
                required=["name", "estimated_weight_g", "calories", "protein_g", "carbs_g", "fat_g"],
                properties={
                    "name": genai.types.Schema(type=genai.types.Type.STRING),
                    "estimated_weight_g": genai.types.Schema(type=genai.types.Type.NUMBER),
                    "calories": genai.types.Schema(type=genai.types.Type.NUMBER),
                    "protein_g": genai.types.Schema(type=genai.types.Type.NUMBER),
                    "carbs_g": genai.types.Schema(type=genai.types.Type.NUMBER),
                    "fat_g": genai.types.Schema(type=genai.types.Type.NUMBER),
                },
            ),
        ),
    },
)

_SYSTEM_INSTRUCTION = (
    "Eres un nutricionista experto y un sistema de visión artificial de alta precisión. "
    "Tu tarea es analizar la imagen de comida proporcionada, identificar los ingredientes "
    "visibles, estimar el tamaño de la porción promedio en gramos y calcular los "
    "macronutrientes basándote en bases de datos nutricionales estándar. "
    "Si la imagen no contiene comida o es irreconocible, marca el campo 'success' como "
    "falso y devuelve un mensaje explicativo en 'error', dejando los demás campos en 0. "
    "Las calorías deben estar en kcal y los macros en gramos."
)

_GENERATE_CONFIG = types.GenerateContentConfig(
    temperature=settings.GEMINI_TEMPERATURE,
    response_mime_type="application/json",
    system_instruction=[types.Part.from_text(text=_SYSTEM_INSTRUCTION)],
    response_schema=_RESPONSE_SCHEMA,
)

class GeminiNutritionService:
    """Encapsula toda la lógica de comunicación con la API de Gemini."""

    def __init__(self) -> None:
        self._client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_meal(self, image_bytes: bytes, mime_type: str) -> MealAnalysisResponse:
        """
        Envía la imagen a Gemini y devuelve el análisis nutricional
        deserializado como un objeto Pydantic.
        """
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    types.Part.from_text(text="Analiza este platillo y calcula sus macros"),
                ],
            )
        ]

        response = self._client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=_GENERATE_CONFIG,
        )

        return MealAnalysisResponse(**json.loads(response.text))


# Singleton reutilizable en toda la app
gemini_nutrition_service = GeminiNutritionService()
