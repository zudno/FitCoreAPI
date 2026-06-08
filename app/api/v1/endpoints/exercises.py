from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from app.api.v1.deps import get_current_user, get_owned_exercise, get_editable_exercise
from app.core.database import get_session
from app.core.exceptions import MuscleGroupNotFoundError, ExerciseAlreadyExistsError, InvalidImageError, InvalidGifError
from app.models.user import User
from app.models.exercise import Exercise
from app.models.muscle_group import MuscleGroup
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseRead, ExerciseDetail
from app.services.storage_service import storage_service

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get(
    "/",
    response_model=List[ExerciseDetail],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los ejercicios disponibles",
)
def get_exercises(
    muscle_group_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[ExerciseDetail]:
    """
    Retorna la lista de todos los ejercicios del sistema (globales) 
    más los ejercicios personalizados creados por el usuario actual.
    Soporta filtrado opcional por grupo muscular.
    """
    # Consulta: Ejercicios del sistema (user_id IS NULL) OR Ejercicios del usuario
    statement = select(Exercise).where(
        (Exercise.user_id == None) | (Exercise.user_id == current_user.id)
    )
    
    if muscle_group_id:
        statement = statement.where(Exercise.muscle_group_id == muscle_group_id)
        
    statement = statement.order_by(Exercise.name.asc())
    exercises = session.exec(statement).all()
    return exercises


@router.get(
    "/{exercise_id}",
    response_model=ExerciseDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener un ejercicio por ID",
)
def get_exercise(
    exercise: Exercise = Depends(get_owned_exercise),
) -> ExerciseDetail:
    """
    Retorna un ejercicio específico si es global o si pertenece al usuario actual.
    """
    return exercise


@router.post(
    "/",
    response_model=ExerciseRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un ejercicio personalizado",
)
def create_exercise(
    exercise_in: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ExerciseRead:
    """
    Crea un nuevo ejercicio personalizado asignado al usuario actual.
    Valida que el grupo muscular principal proporcionado exista.
    """
    # Validar grupo muscular
    muscle_group = session.get(MuscleGroup, exercise_in.muscle_group_id)
    if not muscle_group:
        raise MuscleGroupNotFoundError()
        
    # Validar que no haya un ejercicio propio del mismo usuario con el mismo nombre
    existing_statement = select(Exercise).where(
        Exercise.name == exercise_in.name,
        Exercise.user_id == current_user.id
    )
    existing = session.exec(existing_statement).first()
    if existing:
        raise ExerciseAlreadyExistsError()
        
    exercise = Exercise(
        **exercise_in.model_dump(),
        user_id=current_user.id
    )
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


@router.put(
    "/{exercise_id}",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un ejercicio personalizado",
)
def update_exercise(
    exercise_in: ExerciseUpdate,
    exercise: Exercise = Depends(get_editable_exercise),
    session: Session = Depends(get_session),
) -> ExerciseRead:
    """
    Actualiza los datos de un ejercicio personalizado.
    No se permite modificar ejercicios del sistema (globales).
    """
    # Si se actualiza el grupo muscular, validar su existencia
    if exercise_in.muscle_group_id is not None:
        muscle_group = session.get(MuscleGroup, exercise_in.muscle_group_id)
        if not muscle_group:
            raise MuscleGroupNotFoundError()
            
    # Aplicar cambios parciales de forma segura
    update_data = exercise_in.model_dump(exclude_unset=True)
    exercise.sqlmodel_update(update_data)
        
    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


@router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un ejercicio personalizado",
)
def delete_exercise(
    exercise: Exercise = Depends(get_editable_exercise),
    session: Session = Depends(get_session),
) -> None:
    """
    Elimina permanentemente un ejercicio personalizado creado por el usuario.
    No se permite eliminar ejercicios globales del sistema.
    """
    session.delete(exercise)
    session.commit()
    return None


@router.post(
    "/{exercise_id}/image",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Subir imagen de un ejercicio personalizado",
)
async def upload_exercise_image(
    file: UploadFile = File(...),
    exercise: Exercise = Depends(get_editable_exercise),
    session: Session = Depends(get_session),
) -> ExerciseRead:
    """
    Sube una imagen para un ejercicio personalizado del usuario.
    Si ya tenía imagen, la anterior se elimina del bucket.
    Solo el propietario del ejercicio puede subir imágenes.
    """
    if not file.content_type.startswith("image/"):
        raise InvalidImageError()

    # Borrar imagen anterior si existe
    if exercise.image_url:
        storage_service.delete_exercise_media(exercise.image_url)

    image_url = await storage_service.upload_exercise_image(file, str(exercise.id))
    exercise.image_url = image_url

    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise


@router.post(
    "/{exercise_id}/gif",
    response_model=ExerciseRead,
    status_code=status.HTTP_200_OK,
    summary="Subir GIF de un ejercicio personalizado",
)
async def upload_exercise_gif(
    file: UploadFile = File(...),
    exercise: Exercise = Depends(get_editable_exercise),
    session: Session = Depends(get_session),
) -> ExerciseRead:
    """
    Sube un GIF para un ejercicio personalizado del usuario.
    Si ya tenía GIF almacenado en GCS, el anterior se elimina.
    Solo el propietario del ejercicio puede subir GIFs.
    """
    if file.content_type != "image/gif":
        raise InvalidGifError()

    # Borrar GIF anterior si estaba alojado en GCS
    if exercise.gif_url and "storage.googleapis.com" in exercise.gif_url:
        storage_service.delete_exercise_media(exercise.gif_url)

    gif_url = await storage_service.upload_exercise_gif(file, str(exercise.id))
    exercise.gif_url = gif_url

    session.add(exercise)
    session.commit()
    session.refresh(exercise)
    return exercise
