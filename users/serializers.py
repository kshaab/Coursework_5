from typing import Dict, Any

from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserCreateSerializer(ModelSerializer):
    """Сериализатор создания пользователя"""
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "phone_number", "town")

    def create(self, validated_data: Dict[str, Any]) -> User:
        """Создает пользователя с хешированным паролем"""
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class UserPublicSerializer(ModelSerializer):
    """Сериализатор для публичного просмотра пользователей"""
    class Meta:
        model = User
        fields = ("id", "town", "avatar")


class UserPrivateSerializer(ModelSerializer):
    """Сериализатор для приватного просмотра профиля"""
    payments = SerializerMethodField()

    class Meta:
        model = User
        exclude = ("password",)


class UserUpdateSerializer(ModelSerializer):
    """Сериализатор для обновления профиля"""
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "town",
            "avatar",
        )