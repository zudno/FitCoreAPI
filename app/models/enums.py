from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"  # Poco o nada de ejercicio
    LIGHT = "light"          # Ejercicio ligero 1-3 días/semana
    MODERATE = "moderate"    # Ejercicio moderado 3-5 días/semana
    VERY_ACTIVE = "very"     # Ejercicio intenso 6-7 días/semana
    EXTRA_ACTIVE = "extra"   # Ejercicio muy intenso o trabajo físico


class FitnessGoal(str, Enum):
    LOSE_WEIGHT = "lose"
    MAINTAIN_WEIGHT = "maintain"
    GAIN_MUSCLE = "gain"


class UnitSystem(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class RoutineGoal(str, Enum):
    HYPERTROPHY = "hypertrophy"
    STRENGTH = "strength"
    DEFINITION = "definition"
    ENDURANCE = "endurance"


class RoutineLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SetType(str, Enum):
    NORMAL = "normal"
    WARMUP = "warmup"
    DROP_SET = "drop_set"
    FAILURE = "failure"


class AuthProvider(str, Enum):
    NATIVE = "native"
    GOOGLE = "google"

