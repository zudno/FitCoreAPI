from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.api.v1.deps import get_current_user
from app.core.database import get_session
from app.core.exceptions import (
    WorkoutSessionNotFoundError,
    WorkoutSessionAlreadyEndedError,
    WorkoutSetNotFoundError,
    ExerciseNotFoundError,
)
from app.models.user import User
from app.models.exercise import Exercise
from app.models.workout import WorkoutSession, WorkoutSet
from app.schemas.workout import (
    WorkoutSessionCreate,
    WorkoutSessionUpdate,
    WorkoutSessionRead,
    WorkoutSessionDetail,
    WorkoutSetCreate,
    WorkoutSetUpdate,
    WorkoutSetRead,
)

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.post(
    "/",
    response_model=WorkoutSessionDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar una nueva sesión de entrenamiento",
)
def start_workout_session(
    session_in: WorkoutSessionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSessionDetail:
    """
    Inicia una nueva sesión de entrenamiento. 
    Si el usuario tiene otra sesión activa (sin finalizar), la finaliza automáticamente en este momento.
    Permite opcionalmente registrar series de forma inmediata en lote (ej. sincronización offline).
    """
    # Auto-finalizar sesiones activas previas
    active_stmt = select(WorkoutSession).where(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.ended_at == None,
    )
    active_sessions = session.exec(active_stmt).all()
    now_utc = datetime.now(timezone.utc)
    for active_s in active_sessions:
        active_s.ended_at = now_utc
        session.add(active_s)

    # 1. Crear la cabecera de la sesión
    workout_session = WorkoutSession(
        workout_program_id=session_in.workout_program_id,
        routine_id=session_in.routine_id,
        notes=session_in.notes,
        started_at=session_in.started_at or now_utc,
        ended_at=session_in.ended_at,
        user_id=current_user.id,
    )
    session.add(workout_session)
    session.flush()

    # 2. Agregar series si vienen en lote
    if session_in.sets:
        for set_in in session_in.sets:
            # Validar ejercicio
            exercise = session.get(Exercise, set_in.exercise_id)
            if not exercise or (exercise.user_id is not None and exercise.user_id != current_user.id):
                raise ExerciseNotFoundError()

            workout_set = WorkoutSet(
                session_id=workout_session.id,
                exercise_id=set_in.exercise_id,
                set_number=set_in.set_number,
                set_type=set_in.set_type,
                reps_done=set_in.reps_done,
                weight_kg=set_in.weight_kg,
                rir=set_in.rir,
                rpe=set_in.rpe,
                completed=set_in.completed,
                notes=set_in.notes,
                routine_exercise_id=set_in.routine_exercise_id,
            )
            session.add(workout_set)

    session.commit()
    session.refresh(workout_session)
    return workout_session


@router.get(
    "/",
    response_model=List[WorkoutSessionRead],
    status_code=status.HTTP_200_OK,
    summary="Obtener historial de sesiones de entrenamiento",
)
def get_workout_sessions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[WorkoutSessionRead]:
    """
    Retorna la lista de todas las sesiones de entrenamiento del usuario, ordenadas por fecha de inicio descendente.
    """
    statement = select(WorkoutSession).where(
        WorkoutSession.user_id == current_user.id
    ).order_by(WorkoutSession.started_at.desc())
    sessions = session.exec(statement).all()
    return sessions


@router.get(
    "/active",
    response_model=WorkoutSessionDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener la sesión de entrenamiento actualmente activa",
)
def get_active_workout_session(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSessionDetail:
    """
    Busca y retorna la sesión de entrenamiento que no ha finalizado (ended_at es nulo).
    Si no existe ninguna sesión activa, retorna un error 404.
    """
    statement = select(WorkoutSession).where(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.ended_at == None,
    ).order_by(WorkoutSession.started_at.desc())
    active_session = session.exec(statement).first()

    if not active_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay una sesión de entrenamiento activa.",
        )
    return active_session


@router.get(
    "/{session_id}",
    response_model=WorkoutSessionDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener detalles de una sesión de entrenamiento por ID",
)
def get_workout_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSessionDetail:
    """
    Retorna los detalles completos de una sesión de entrenamiento (incluyendo todas sus series e información del ejercicio).
    """
    workout_session = session.get(WorkoutSession, session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSessionNotFoundError()
    return workout_session


@router.post(
    "/{session_id}/end",
    response_model=WorkoutSessionRead,
    status_code=status.HTTP_200_OK,
    summary="Finalizar una sesión de entrenamiento activa",
)
def end_workout_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSessionRead:
    """
    Finaliza una sesión de entrenamiento activa registrando la marca de tiempo de fin en UTC.
    """
    workout_session = session.get(WorkoutSession, session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSessionNotFoundError()

    if workout_session.ended_at is not None:
        raise WorkoutSessionAlreadyEndedError()

    workout_session.ended_at = datetime.now(timezone.utc)
    session.add(workout_session)
    session.commit()
    session.refresh(workout_session)
    return workout_session


@router.post(
    "/{session_id}/sets",
    response_model=WorkoutSetRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar dinámicamente una nueva serie en la sesión activa",
)
def add_workout_set(
    session_id: UUID,
    set_in: WorkoutSetCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSetRead:
    """
    Registra una serie realizada en tiempo real dentro de una sesión de entrenamiento activa.
    """
    workout_session = session.get(WorkoutSession, session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSessionNotFoundError()

    if workout_session.ended_at is not None:
        raise WorkoutSessionAlreadyEndedError()

    # Validar ejercicio accesible
    exercise = session.get(Exercise, set_in.exercise_id)
    if not exercise or (exercise.user_id is not None and exercise.user_id != current_user.id):
        raise ExerciseNotFoundError()

    workout_set = WorkoutSet(
        session_id=workout_session.id,
        exercise_id=set_in.exercise_id,
        set_number=set_in.set_number,
        set_type=set_in.set_type,
        reps_done=set_in.reps_done,
        weight_kg=set_in.weight_kg,
        rir=set_in.rir,
        rpe=set_in.rpe,
        completed=set_in.completed,
        notes=set_in.notes,
        routine_exercise_id=set_in.routine_exercise_id,
    )
    session.add(workout_set)
    session.commit()
    session.refresh(workout_set)
    return workout_set


@router.put(
    "/sets/{set_id}",
    response_model=WorkoutSetRead,
    status_code=status.HTTP_200_OK,
    summary="Modificar/corregir una serie registrada anteriormente",
)
def update_workout_set(
    set_id: UUID,
    set_in: WorkoutSetUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSetRead:
    """
    Permite modificar los datos de una serie específica (ej. corrección de peso o repeticiones erróneas).
    Solo se permite si la sesión a la que pertenece sigue activa/abierta.
    """
    workout_set = session.get(WorkoutSet, set_id)
    if not workout_set:
        raise WorkoutSetNotFoundError()

    # Validar que pertenezca al usuario
    workout_session = session.get(WorkoutSession, workout_set.session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSetNotFoundError()

    # Validar que la sesión no esté finalizada
    if workout_session.ended_at is not None:
        raise WorkoutSessionAlreadyEndedError()

    # Validar ejercicio si se cambia
    update_data = set_in.model_dump(exclude_unset=True)
    if "exercise_id" in update_data:
        exercise = session.get(Exercise, set_in.exercise_id)
        if not exercise or (exercise.user_id is not None and exercise.user_id != current_user.id):
            raise ExerciseNotFoundError()

    # Aplicar cambios parciales
    for key, value in update_data.items():
        setattr(workout_set, key, value)

    session.add(workout_set)
    session.commit()
    session.refresh(workout_set)
    return workout_set


@router.delete(
    "/sets/{set_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una serie registrada de la sesión activa",
)
def delete_workout_set(
    set_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """
    Elimina permanentemente una serie de la sesión de entrenamiento.
    Solo se permite si la sesión de entrenamiento sigue activa/abierta.
    """
    workout_set = session.get(WorkoutSet, set_id)
    if not workout_set:
        raise WorkoutSetNotFoundError()

    # Validar propiedad
    workout_session = session.get(WorkoutSession, workout_set.session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSetNotFoundError()

    # Validar que la sesión siga activa
    if workout_session.ended_at is not None:
        raise WorkoutSessionAlreadyEndedError()

    session.delete(workout_set)
    session.commit()
    return None
