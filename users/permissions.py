from typing import Any

from rest_framework import permissions
from rest_framework.views import APIView


class IsOwner(permissions.BasePermission):
    """Права доступа пользователей к своим привычкам"""

    def has_object_permission(self, request: Any, view: APIView, obj: Any) -> bool:
        """Проверяет, является ли пользователь владельцем"""
        if obj.user == request.user:
            return True
        return False


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """Публичные права доступа для просмотра привычек"""

    def has_object_permission(self, request: Any, view: APIView, obj: Any) -> Any:
        """Проверяет, что другие пользователи могут просматривать только публичные привычки"""
        if obj.user == request.user:
            return True
        if obj.is_public and request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Приватные права доступа к профилю для владельца, остальные могут только просматривать"""

    def has_object_permission(self, request: Any, view: APIView, obj: Any) -> Any:
        """Разрешает редактирование профиля только владельцем"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
