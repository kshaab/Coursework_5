from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import generics

from habits.models import Habit
from habits.pagination import HabitPageNumberPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner, IsOwnerOrPublicReadOnly


@extend_schema(
    summary="Создание привычки",
    description="Создает новую привычку и привязывает ее к текущему пользователю (нужно быть зарегистрированным).",
    request=HabitSerializer,
    responses=HabitSerializer,
)
class HabitCreateView(CreateAPIView):
    """Эндпоинт создания привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: Serializer) -> None:
        """Привязывает привычку к пользователю"""
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Список привычек",
    description="Возвращает список привычек, при этом для публичного просмотра доступны только публичные привычки.",
    request=HabitSerializer,
    responses=HabitSerializer,
)
class HabitListView(generics.ListAPIView):
    """Эндпоинт просмотра списка привычек"""

    serializer_class = HabitSerializer
    pagination_class = HabitPageNumberPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublicReadOnly]

    def get_queryset(self) -> QuerySet:
        """Возвращает список приватных привычек пользователю, публичных для общего просмотра"""
        user = self.request.user
        own_habits = Habit.objects.filter(user=user)
        public_habits = Habit.objects.filter(is_public=True).exclude(user=user)
        return own_habits.union(public_habits).order_by("time")


@extend_schema(
    summary="Детали привычки",
    description="Возвращает детальную информацию о привычке пользователю.",
    request=HabitSerializer,
    responses=HabitSerializer,
)
class HabitRetrieveView(generics.RetrieveAPIView):
    """Эндпоинт просмотра одной привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrPublicReadOnly]


@extend_schema(
    summary="Редактирование привычки",
    description="Обновляет существующую привычку, обновление доступно только владельцу.",
    request=HabitSerializer,
    responses=HabitSerializer,
)
class HabitUpdateView(UpdateAPIView):
    """Эндпоинт редактирования привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


@extend_schema(
    summary="Удаление привычки",
    description="Удаляет привычку, удаление доступно только владельцу.",
    request=HabitSerializer,
    responses=HabitSerializer,
)
class HabitDestroyView(DestroyAPIView):
    """Эндпоинт удаления привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
