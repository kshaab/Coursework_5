from django.db import models
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, verbose_name="Место выполнения привычки")
    time = models.TimeField(verbose_name="Время, когда необходимо выполнять привычку")
    action = models.CharField(max_length=100, verbose_name="Выполняемое действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Связанная привычка")
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность выполнения привычки в днях")
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение привычки в секундах")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.place

