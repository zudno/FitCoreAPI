from datetime import date
from app.models.profile import Profile
from app.models.enums import Gender, ActivityLevel, FitnessGoal

class NutritionService:
    def calculate_daily_targets(self, profile: Profile):
        """
        Calcula las metas diarias de calorías y macros usando la fórmula de Mifflin-St Jeor.
        """
        # 1. Calcular Edad
        today = date.today()
        age = today.year - profile.date_of_birth.year - (
            (today.month, today.day) < (profile.date_of_birth.month, profile.date_of_birth.day)
        )
        
        # 2. Calcular BMR (Tasa Metabólica Basal)
        if profile.gender == Gender.MALE:
            bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * age) + 5
        else:
            bmr = (10 * profile.weight) + (6.25 * profile.height) - (5 * age) - 161
            
        # 3. Factor de Actividad (TDEE - Gasto Energético Total Diario)
        activity_factors = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.VERY_ACTIVE: 1.725,
            ActivityLevel.EXTRA_ACTIVE: 1.9
        }
        tdee = bmr * activity_factors.get(profile.activity_level, 1.2)
        
        # 4. Ajuste según la Meta (Déficit o Superávit)
        goal_adjustments = {
            FitnessGoal.LOSE_WEIGHT: -500,      # Déficit para perder peso
            FitnessGoal.MAINTAIN_WEIGHT: 0,    # Mantenimiento
            FitnessGoal.GAIN_MUSCLE: 300       # Superávit moderado para ganar músculo
        }
        target_calories = tdee + goal_adjustments.get(profile.goal, 0)
        
        # 5. Distribución de Macros (P: 30%, G: 25%, C: 45%)
        # Proteína: 4 kcal/g | Carbohidratos: 4 kcal/g | Grasas: 9 kcal/g
        protein_kcal = target_calories * 0.30
        fat_kcal = target_calories * 0.25
        carbs_kcal = target_calories * 0.45
        
        return {
            "daily_calories": round(target_calories),
            "daily_protein_g": round(protein_kcal / 4),
            "daily_carbs_g": round(carbs_kcal / 4),
            "daily_fat_g": round(fat_kcal / 9),
        }

nutrition_service = NutritionService()
