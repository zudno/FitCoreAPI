from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.api.v1.deps import get_current_user
from app.core.database import get_session
from app.core.exceptions import MuscleGroupNotFoundError, MuscleGroupAlreadyExistsError
from app.models.user import User
from app.models.muscle_group import MuscleGroup
from app.schemas.muscle_group import MuscleGroupCreate, MuscleGroupRead

router = APIRouter(prefix="/muscle-groups", tags=["Muscle Groups"])


@router.get(
    "/",
    response_model=List[MuscleGroupRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los grupos musculares",
)
def get_muscle_groups(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[MuscleGroupRead]:
    """
    Retorna la lista de todos los grupos musculares registrados en el sistema.
    """
    statement = select(MuscleGroup).order_by(MuscleGroup.name.asc())
    muscle_groups = session.exec(statement).all()
    return muscle_groups


@router.post(
    "/",
    response_model=MuscleGroupRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un grupo muscular",
)
def create_muscle_group(
    muscle_group_in: MuscleGroupCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> MuscleGroupRead:
    """
    Crea un nuevo grupo muscular en el sistema (el nombre debe ser único).
    """
    # Verificar unicidad del nombre
    statement = select(MuscleGroup).where(MuscleGroup.name == muscle_group_in.name)
    existing = session.exec(statement).first()
    if existing:
        raise MuscleGroupAlreadyExistsError()
    
    muscle_group = MuscleGroup(**muscle_group_in.model_dump())
    session.add(muscle_group)
    session.commit()
    session.refresh(muscle_group)
    return muscle_group


@router.get(
    "/{muscle_group_id}",
    response_model=MuscleGroupRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener un grupo muscular por ID",
)
def get_muscle_group(
    muscle_group_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> MuscleGroupRead:
    """
    Busca y retorna un grupo muscular específico por su ID.
    """
    muscle_group = session.get(MuscleGroup, muscle_group_id)
    if not muscle_group:
        raise MuscleGroupNotFoundError()
    return muscle_group
