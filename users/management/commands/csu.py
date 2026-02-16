from typing import Any

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперпользователя"""

    def handle(self, *args: Any, **options: Any) -> None:
        """Создает администратора"""
        user = User.objects.create(email="admin@example.com")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
