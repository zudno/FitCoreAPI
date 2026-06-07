from app.core.exceptions.auth import (
    InactiveUserError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    InvalidTokenError,
    UserAlreadyExistsError,
)
from app.core.exceptions.handlers import register_exception_handlers
from app.core.exceptions.meals import EmptyFileError, InvalidImageError
from app.core.exceptions.profile import ProfileNotFoundError
from app.core.exceptions.exercises import (
    MuscleGroupNotFoundError,
    ExerciseNotFoundError,
    ExerciseAccessDeniedError,
)
from app.core.exceptions.routines import RoutineNotFoundError
from app.core.exceptions.workouts import (
    WorkoutSessionNotFoundError,
    WorkoutSessionAlreadyEndedError,
    WorkoutSetNotFoundError,
)

__all__ = [
    # Auth
    "UserAlreadyExistsError",
    "InvalidCredentialsError",
    "InactiveUserError",
    "InvalidTokenError",
    "InvalidRefreshTokenError",
    # Meals
    "InvalidImageError",
    "EmptyFileError",
    # Profile
    "ProfileNotFoundError",
    # Exercises & Muscle Groups
    "MuscleGroupNotFoundError",
    "ExerciseNotFoundError",
    "ExerciseAccessDeniedError",
    # Routines
    "RoutineNotFoundError",
    # Workouts
    "WorkoutSessionNotFoundError",
    "WorkoutSessionAlreadyEndedError",
    "WorkoutSetNotFoundError",
    # Handlers
    "register_exception_handlers",
]
