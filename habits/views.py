from typing import Any

from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from rest_framework.viewsets import generics

from habits.pagination import HabitPageNumberPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner, IsOwnerOrPublicReadOnly


class HabitCreateView(CreateAPIView):
    """Эндпоинт создания привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer) -> None:
        """Привязывает привычку к пользователю"""
        serializer.save(user=self.request.user)

class HabitListView(generics.ListAPIView):
    """Эндпоинт просмотра списка привычек"""
    serializer_class = HabitSerializer
    pagination_class = HabitPageNumberPagination
    permission_classes = [IsOwnerOrPublicReadOnly]

    def get_queryset(self) -> QuerySet:
        """Возвращает список приватных привычек пользователю, публичных для общего просмотра"""
        user = self.request.user
        own_habits = Habit.objects.filter(user=user)
        public_habits = Habit.objects.filter(is_public=True).exclude(user=user)
        return own_habits.union(public_habits).distinct()

class HabitRetrieveView(generics.RetrieveAPIView):
    """Эндпоинт просмотра одной привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

class HabitUpdateView(UpdateAPIView):
    """Эндпоинт редактирования привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

class HabitDestroyView(DestroyAPIView):
    """Эндпоинт удаления привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


