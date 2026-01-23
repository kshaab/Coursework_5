from rest_framework.serializers import ValidationError



class HabitValidator:
    """Валидатор привычки"""

    @staticmethod
    def validate_reward_or_related(instance):
        """Исключает одновременный выбор связанной привычки и указание вознаграждения"""
        if instance.is_pleasant:
            if instance.reward or instance.related_habit:
                raise ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        else:
            if instance.reward and instance.related_habit:
                raise ValidationError("Полезная привычка не может иметь одновременно и вознаграждение, и связанную привычку.")
            if not instance.reward and not instance.related_habit:
                raise ValidationError("Полезная привычка должна иметь либо вознаграждение, либо связанную привычку.")

    @staticmethod
    def validate_duration(instance):
        """Проверяет, что время выполнения привычки не больше 120 секунд"""
        if instance.duration > 120:
            raise ValidationError("Время выполнения привычки не должно превышать 120 секунд.")

    @staticmethod
    def validate_related(instance):
        """Проверяет, что связанная привычка только приятная"""
        if instance.related:
            if not instance.related_habit.is_pleasant:
                raise ValidationError("В связанную привычку могут попадать только приятные привычки.")

    @staticmethod
    def validate_periodicity(instance):
        """Проверяет, что привычка выполняется минимум раз в 7 дней"""
        if instance.periodicity < 1:
            raise ValidationError("Минимальная периодичность привычки 1 день.")
        if instance.periodicity > 7:
            raise ValidationError("За 7 дней необходимо выполнить привычку хотя бы один раз.")



    def __call__(self, instance):
        self.validate_reward_or_related(instance)
        self.validate_duration(instance)
        self.validate_related(instance)
        self.validate_periodicity(instance)




