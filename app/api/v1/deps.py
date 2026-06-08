from uuid import UUID
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.exceptions import (
    InactiveUserError,
    InvalidTokenError,
    ExerciseNotFoundError,
    ExerciseAccessDeniedError,
    WorkoutProgramNotFoundError,
    RoutineNotFoundError,
    WorkoutSessionNotFoundError,
    WorkoutSetNotFoundError,
    NoActiveWorkoutSessionError,
)
from app.core.security import decode_token
from app.models.user import User
from app.models.exercise import Exercise
from app.models.workout_program import WorkoutProgram
from app.models.routine import Routine
from app.models.workout import WorkoutSession, WorkoutSet

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    """
    Extrae y valida el JWT del header Authorization: Bearer <token>.
    Inyectable en cualquier endpoint que requiera autenticación.
    """
    try:
        email = decode_token(credentials.credentials, expected_type="access")
    except JWTError:
        raise InvalidTokenError()

    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise InvalidTokenError()

    if not user.is_active:
        raise InactiveUserError()

    return user


def get_owned_exercise(
    exercise_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Exercise:
    """
    Valida la existencia de un ejercicio y que el usuario actual tenga acceso a él
    (que sea global o de su propiedad).
    """
    exercise = session.get(Exercise, exercise_id)
    if not exercise or (exercise.user_id is not None and exercise.user_id != current_user.id):
        raise ExerciseNotFoundError()
    return exercise


def get_editable_exercise(
    exercise: Exercise = Depends(get_owned_exercise),
) -> Exercise:
    """
    Valida que el ejercicio pertenezca al usuario y sea editable (no global).
    """
    if exercise.user_id is None:
        raise ExerciseAccessDeniedError()
    return exercise


def get_owned_workout_program(
    program_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutProgram:
    """
    Valida la existencia y pertenencia de un programa de entrenamiento.
    """
    program = session.get(WorkoutProgram, program_id)
    if not program or program.user_id != current_user.id:
        raise WorkoutProgramNotFoundError()
    return program


def get_owned_routine(
    routine_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Routine:
    """
    Valida la existencia de una rutina y que pertenezca a un programa del usuario actual.
    """
    routine = session.get(Routine, routine_id)
    if not routine:
        raise RoutineNotFoundError()

    # Validar que el programa padre pertenezca al usuario
    program = session.get(WorkoutProgram, routine.program_id)
    if not program or program.user_id != current_user.id:
        raise RoutineNotFoundError()

    return routine


def get_owned_workout_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSession:
    """
    Valida la existencia y pertenencia de una sesión de entrenamiento.
    """
    workout_session = session.get(WorkoutSession, session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSessionNotFoundError()
    return workout_session


def get_active_workout_session(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSession:
    """
    Retorna la sesión de entrenamiento actualmente activa para el usuario,
    o lanza un error 404 si no hay ninguna activa.
    """
    statement = select(WorkoutSession).where(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.ended_at == None,
    ).order_by(WorkoutSession.started_at.desc())
    active_session = session.exec(statement).first()

    if not active_session:
        raise NoActiveWorkoutSessionError()
    return active_session


def get_owned_workout_set(
    set_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> WorkoutSet:
    """
    Valida la existencia de una serie de entrenamiento y que pertenezca a una
    sesión propiedad del usuario actual.
    """
    workout_set = session.get(WorkoutSet, set_id)
    if not workout_set:
        raise WorkoutSetNotFoundError()

    # Validar sesión asociada
    workout_session = session.get(WorkoutSession, workout_set.session_id)
    if not workout_session or workout_session.user_id != current_user.id:
        raise WorkoutSetNotFoundError()

    return workout_set