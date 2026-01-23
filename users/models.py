from typing import Any, ClassVar, List

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    town = models.CharField(max_length=35, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    tg_chat_id = models.CharField(max_length=50, verbose_name="Телеграм chat_id", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[List[str]] = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> Any:
        return self.email
