from typing import List, Type

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import User
from users.pagination import UserPageNumberPagination
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserCreateSerializer, UserPrivateSerializer, UserPublicSerializer, UserUpdateSerializer


@extend_schema_view(
    create=extend_schema(
        summary="Создание пользователя/регистрация",
        description="Создает нового пользователя.",
        request=UserCreateSerializer,
        responses=UserCreateSerializer,
    ),
    retrieve=extend_schema(
        summary="Детали пользователя",
        description="Возвращает профиль пользователя с данными о пользователе, приватные данные остаются в закрытом доступе.",
        responses=UserPrivateSerializer,
    ),
    list=extend_schema(
        summary="Список пользователей",
        description="Возвращает список всех пользователей.",
        responses=UserPublicSerializer,
    ),
    update=extend_schema(
        summary="Обновление пользователя",
        description="Обновляет данные существующего пользователя, обновление доступно только владельцу аккаунта.",
        request=UserUpdateSerializer,
        responses=UserUpdateSerializer,
    ),
    partial_update=extend_schema(
        summary="Частичное обновление пользователя",
        description="Частично обновляет данные пользователя, обновление доступно только владельцу аккаунта.",
        request=UserUpdateSerializer,
        responses=UserUpdateSerializer,
    ),
    destroy=extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя.",
        responses=None,
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """Эндпоинт для пользователей"""

    queryset = User.objects.all()
    pagination_class = UserPageNumberPagination

    def get_permissions(self) -> List[permissions.BasePermission]:
        """Получает права доступа для действий"""
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_serializer_class(self) -> Type[Serializer]:
        """Получает сериализатор для текущего действия"""
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "retrieve":
            if self.request.user == self.get_object():
                return UserPrivateSerializer
            return UserPublicSerializer
        elif self.action == "list":
            return UserPublicSerializer
        return UserPublicSerializer
