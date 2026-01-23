from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Права доступа пользователей к своим привычкам"""
    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь владельцем"""
        if obj.user == request.user:
            return True
        return False


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """Публичные права доступа"""
    def has_object_permission(self, request, view, obj):
        """Проверяет, что другие пользователи могут просматривать только публичные привычки"""
        if obj.user == request.user:
            return True
        if obj.is_public and request.method in permissions.SAFE_METHODS:
            return True
        return False