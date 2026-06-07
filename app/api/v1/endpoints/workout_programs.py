from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.api.v1.deps import get_current_user
from app.core.database import get_session
from app.core.exceptions import RoutineNotFoundError, ExerciseNotFoundError
from app.models.user import User
from app.models.exercise import Exercise
from app.models.workout_program import WorkoutProgram
from app.models.routine import Routine, RoutineExercise
from app.services.storage_service import storage_service
from app.schemas.workout_program import (
    WorkoutProgramCreate,
    WorkoutProgramUpdate,
    WorkoutProgramRead,
    WorkoutProgramDetail,
)

router = APIRouter(prefix="/workout-programs", tags=["Workout Programs"])


def _assert_program_owned(program: WorkoutProgram | None, user_id: UUID) -> WorkoutProgram:
    if not program or program.user_id != user_id:
        raise RoutineNotFoundError()
    return program


def _deactivate_others(session: Session, user_id: UUID) -> None:
    stmt = select(WorkoutProgram).where(WorkoutProgram.user_id == user_id, WorkoutProgram.is_active == True)
    for p in session.exec(stmt).all():
        p.is_active = False
        session.add(p)


@router.post(
    "/",
    response_model=WorkoutProgramDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo programa de entrenamiento",
)
def create_workout_program(
    program_in: WorkoutProgramCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgramDetail:
    if program_in.is_active:
        _deactivate_others(session, current_user.id)

    program = WorkoutProgram(
        user_id=current_user.id,
        name=program_in.name,
        goal=program_in.goal,
        level=program_in.level,
        is_active=program_in.is_active,
        description=program_in.description,
        image_url=program_in.image_url,
    )
    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@router.get(
    "/",
    response_model=List[WorkoutProgramRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los programas del usuario",
)
def get_workout_programs(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[WorkoutProgramRead]:
    stmt = select(WorkoutProgram).where(WorkoutProgram.user_id == current_user.id).order_by(WorkoutProgram.created_at.desc())
    return session.exec(stmt).all()


@router.get(
    "/{program_id}",
    response_model=WorkoutProgramDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener un programa con sus rutinas y ejercicios",
)
def get_workout_program(
    program_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgramDetail:
    program = session.get(WorkoutProgram, program_id)
    return _assert_program_owned(program, current_user.id)


@router.put(
    "/{program_id}",
    response_model=WorkoutProgramDetail,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un programa y sus rutinas",
)
def update_workout_program(
    program_id: UUID,
    program_in: WorkoutProgramUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgramDetail:
    program = session.get(WorkoutProgram, program_id)
    _assert_program_owned(program, current_user.id)

    update_data = program_in.model_dump(exclude_unset=True)

    if update_data.get("is_active") is True and not program.is_active:
        _deactivate_others(session, current_user.id)

    for key, value in update_data.items():
        if key != "routines":
            setattr(program, key, value)

    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@router.patch(
    "/{program_id}/activate",
    response_model=WorkoutProgramRead,
    status_code=status.HTTP_200_OK,
    summary="Activar un programa y desactivar los demás",
)
def activate_workout_program(
    program_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgramRead:
    program = session.get(WorkoutProgram, program_id)
    _assert_program_owned(program, current_user.id)

    if not program.is_active:
        _deactivate_others(session, current_user.id)
        program.is_active = True
        session.add(program)
        session.commit()
        session.refresh(program)

    return program


@router.post(
    "/{program_id}/image",
    response_model=WorkoutProgramRead,
    status_code=status.HTTP_200_OK,
    summary="Subir o reemplazar la imagen de un programa",
)
async def upload_program_image(
    program_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgramRead:
    program = session.get(WorkoutProgram, program_id)
    _assert_program_owned(program, current_user.id)

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen (jpg, png, webp).",
        )

    if program.image_url:
        storage_service.delete_program_image(program.image_url)

    program.image_url = await storage_service.upload_program_image(file, str(program_id))

    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@router.delete(
    "/{program_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un programa",
)
def delete_workout_program(
    program_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    program = session.get(WorkoutProgram, program_id)
    _assert_program_owned(program, current_user.id)
    session.delete(program)
    session.commit()
