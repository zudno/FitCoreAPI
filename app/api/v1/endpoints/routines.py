from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID

from app.api.v1.deps import get_current_user, get_owned_workout_program, get_owned_routine
from app.core.database import get_session
from app.core.exceptions import ExerciseNotFoundError
from app.models.user import User
from app.models.exercise import Exercise
from app.models.routine import WorkoutProgram, Routine, RoutineExercise
from app.models.workout_program import WorkoutProgram as WorkoutProgramModel
from app.schemas.routine import (
    RoutineCreate,
    RoutineUpdate,
    RoutineDetail,
)

router = APIRouter(prefix="/routines", tags=["Routines"])

def _build_exercise(routine_id: UUID, ex_in, session: Session, user_id: UUID) -> RoutineExercise:
    exercise = session.get(Exercise, ex_in.exercise_id)
    if not exercise or (exercise.user_id is not None and exercise.user_id != user_id):
        raise ExerciseNotFoundError()
    return RoutineExercise(
        routine_id=routine_id,
        exercise_id=ex_in.exercise_id,
        position=ex_in.position,
        rest_seconds=ex_in.rest_seconds,
        weight_unit=ex_in.weight_unit,
        notes=ex_in.notes,
        sets_config=[s.model_dump(mode='json') for s in ex_in.sets_config] if ex_in.sets_config else None,
    )

@router.post(
    "/",
    response_model=RoutineDetail,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva rutina bajo un programa",
)
def create_routine(
    routine_in: RoutineCreate,
    program: WorkoutProgramModel = Depends(get_owned_workout_program),
    session: Session = Depends(get_session),
) -> RoutineDetail:
    routine = Routine(
        program_id=program.id,
        day_numbers=routine_in.day_numbers,
        label=routine_in.label,
        muscle_focus=routine_in.muscle_focus,
    )
    session.add(routine)
    session.flush()

    for ex_in in (routine_in.exercises or []):
        session.add(_build_exercise(routine.id, ex_in, session, program.user_id))

    session.commit()
    session.refresh(routine)
    return routine


@router.get(
    "/{routine_id}",
    response_model=RoutineDetail,
    status_code=status.HTTP_200_OK,
    summary="Obtener una rutina específica",
)
def get_routine(
    routine: Routine = Depends(get_owned_routine),
) -> RoutineDetail:
    return routine


@router.put(
    "/{routine_id}",
    response_model=RoutineDetail,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una rutina y sus ejercicios",
)
def update_routine(
    routine_in: RoutineUpdate,
    routine: Routine = Depends(get_owned_routine),
    session: Session = Depends(get_session),
) -> RoutineDetail:
    update_data = routine_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key != "exercises":
            setattr(routine, key, value)

    if "exercises" in update_data and routine_in.exercises is not None:
        # Reemplazar los ejercicios existentes
        routine.exercises.clear()
        session.flush()
        user_id = routine.program.user_id
        for ex_in in routine_in.exercises:
            session.add(_build_exercise(routine.id, ex_in, session, user_id))

    session.add(routine)
    session.commit()
    session.refresh(routine)
    return routine


@router.delete(
    "/{routine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una rutina de un programa",
)
def delete_routine(
    routine: Routine = Depends(get_owned_routine),
    session: Session = Depends(get_session),
) -> None:
    session.delete(routine)
    session.commit()
