from habits.models import Habit
from rest_framework.viewsets import ModelViewSet

from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer