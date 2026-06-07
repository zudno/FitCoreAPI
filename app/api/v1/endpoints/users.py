from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.api.v1.deps import get_current_user
from app.core.database import get_session
from app.models.user import User
from app.models.profile import Profile
from app.schemas.user import UserRead
from app.schemas.profile import ProfileCreate, ProfileRead
from app.schemas.meal import DailyNutritionTargets
from app.core.exceptions import ProfileNotFoundError
from app.services.storage_service import storage_service
from app.services.nutrition_service import nutrition_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.put(
    "/me/avatar",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar la foto de perfil del usuario",
)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserRead:
    """
    Sube un archivo a Google Cloud Storage y actualiza la URL del avatar del usuario.
    """
    # 1. Si el usuario ya tenía un avatar, podemos borrar el antiguo (limpieza opcional)
    if current_user.avatar_url:
        storage_service.delete_old_avatar(current_user.avatar_url)

    # 2. Subir el nuevo archivo
    # Usamos el id del usuario para organizar la carpeta en GCS
    public_url = await storage_service.upload_avatar(file, str(current_user.id))

    # 3. Actualizar el registro en la base de datos
    current_user.avatar_url = public_url
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener perfil del usuario actual",
)
def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """
    Devuelve los datos del usuario autenticado.
    """
    return current_user


@router.post(
    "/me/profile",
    response_model=ProfileRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear o actualizar el perfil biométrico del usuario",
)
def create_or_update_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ProfileRead:
    """
    Guarda los datos de onboarding del usuario. Si ya existe un perfil, lo actualiza.
    """
    # Intentar obtener el perfil existente
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()

    if profile:
        # Actualizar datos existentes
        update_data = profile_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(profile, key, value)
        profile.updated_at = datetime.now(timezone.utc)
    else:
        # Crear nuevo perfil
        profile = Profile(
            **profile_in.model_dump(),
            user_id=current_user.id
        )

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.get(
    "/me/profile",
    response_model=ProfileRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener las métricas/perfil del usuario actual",
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ProfileRead:
    """
    Devuelve el perfil biométrico vinculado al usuario autenticado.
    """
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()

    if not profile:
        raise ProfileNotFoundError()

    return profile


@router.get(
    "/me/nutrition-targets",
    response_model=DailyNutritionTargets,
    status_code=status.HTTP_200_OK,
    summary="Obtener metas nutricionales diarias calculadas",
)
def get_nutrition_targets(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DailyNutritionTargets:
    """
    Calcula dinámicamente las calorías y macros objetivo basándose en el perfil actual.
    """
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()

    if not profile:
        raise ProfileNotFoundError()

    return nutrition_service.calculate_daily_targets(profile)
