from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, meals, muscle_groups, exercises, workout_programs, routines, workouts

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(meals.router)
api_router.include_router(muscle_groups.router)
api_router.include_router(exercises.router)
api_router.include_router(workout_programs.router)
api_router.include_router(routines.router)
api_router.include_router(workouts.router)
