from typing import Any

from rest_framework.serializers import ValidationError



class HabitValidator:
    """Валидатор привычки"""

    @staticmethod
    def validate_reward_or_related(data: Any) -> None:
        """Исключает одновременный выбор связанной привычки и указание вознаграждения"""
        is_pleasant = data.get("is_pleasant")
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        if is_pleasant:
            if reward or related_habit:
                raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        else:
            if reward and related_habit:
                raise ValidationError("Полезная привычка не может иметь одновременно и вознаграждение, и связанную привычку.")
            if not reward and not related_habit:
                raise ValidationError("Полезная привычка должна иметь либо вознаграждение, либо связанную привычку.")

    @staticmethod
    def validate_duration(data: Any) -> None:
        duration = data.get("duration")
        """Проверяет, что время выполнения привычки не больше 120 секунд"""
        if duration > 120:
            raise ValidationError("Время выполнения привычки не должно превышать 120 секунд.")

    @staticmethod
    def validate_related(data: Any) -> None:
        """Проверяет, что связанная привычка только приятная"""
        related_habit = data.get("related_habit")
        if related_habit and not related_habit.is_pleasant:
                raise ValidationError("В связанную привычку могут попадать только приятные привычки.")

    @staticmethod
    def validate_periodicity(data: Any) -> None:
        """Проверяет, что привычка выполняется минимум раз в 7 дней"""
        periodicity = data.get("periodicity")
        if periodicity < 1:
            raise ValidationError("Минимальная периодичность привычки 1 день.")
        if periodicity > 7:
            raise ValidationError("За 7 дней необходимо выполнить привычку хотя бы один раз.")


    def __call__(self, data):
        self.validate_reward_or_related(data)
        self.validate_duration(data)
        self.validate_related(data)
        self.validate_periodicity(data)




