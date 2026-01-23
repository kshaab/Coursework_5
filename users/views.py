from typing import List, Type

from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer

from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserCreateSerializer, UserPublicSerializer, UserPrivateSerializer, UserUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Эндпоинт для пользователей"""
    queryset = User.objects.all()

    def get_permissions(self) -> List[permissions.BasePermission]:
        """Получает права доступа для действий"""
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(),IsOwnerOrReadOnly()]

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
