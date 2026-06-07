from datetime import datetime, date, time
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlmodel import Session, select
from typing import List

from app.api.v1.deps import get_current_user
from app.core.database import get_session
from app.core.exceptions import EmptyFileError, InvalidImageError
from app.models.user import User
from app.models.meal import Meal
from app.schemas.meal import MealAnalysisResponse, MealCreate, MealRead
from app.services.gemini_service import gemini_nutrition_service
from app.services.storage_service import storage_service

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.post(
    "/analyze",
    response_model=MealAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analizar imagen de comida",
    description=(
        "Recibe una imagen de un platillo y devuelve su información nutricional completa: "
        "nombre del platillo, peso estimado, calorías totales, macros (proteínas, "
        "carbohidratos, grasas) y desglose por ingrediente."
    ),
)
async def analyze_meal(
    file: UploadFile = File(..., description="Imagen del platillo (JPEG, PNG, WEBP, etc.)"),
    current_user: User = Depends(get_current_user),
) -> MealAnalysisResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise InvalidImageError()

    image_bytes = await file.read()

    if not image_bytes:
        raise EmptyFileError()

    # 1. Subir la imagen a la nube para persistencia
    image_url = await storage_service.upload_meal_image(
        image_bytes=image_bytes,
        mime_type=file.content_type,
        user_id=str(current_user.id)
    )

    # 2. Analizar con Gemini
    analysis_result = await gemini_nutrition_service.analyze_meal(
        image_bytes=image_bytes,
        mime_type=file.content_type,
    )

    # 3. Incluir la URL en la respuesta
    analysis_result.image_url = image_url
    
    return analysis_result


@router.post(
    "/",
    response_model=MealRead,
    status_code=status.HTTP_201_CREATED,
    summary="Guardar una comida en el diario",
)
def save_meal(
    meal_in: MealCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> MealRead:
    """
    Guarda una comida analizada (o ingresada manualmente) en la base de datos del usuario.
    """
    meal = Meal(
        **meal_in.model_dump(),
        user_id=current_user.id
    )
    session.add(meal)
    session.commit()
    session.refresh(meal)
    return meal


@router.get(
    "/",
    response_model=List[MealRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener el historial de comidas del usuario",
)
def get_my_meals(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    target_date: date | None = None,
) -> List[MealRead]:
    """
    Devuelve las comidas registradas por el usuario actual. 
    Por defecto devuelve solo las de HOY.
    """
    if target_date is None:
        target_date = date.today()

    # Definir el inicio y fin del día
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = datetime.combine(target_date, time.max)

    statement = (
        select(Meal)
        .where(Meal.user_id == current_user.id)
        .where(Meal.created_at >= start_of_day)
        .where(Meal.created_at <= end_of_day)
        .order_by(Meal.created_at.desc())
    )
    meals = session.exec(statement).all()
    return meals
