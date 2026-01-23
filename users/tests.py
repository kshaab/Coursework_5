from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        """Создает тестового пользователя и аутентифицирует его."""
        self.user = User(email="teat2@example.com")
        self.user.set_password("12345")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self) -> None:
        """Тестирует создание пользователя."""
        url = reverse("users:users-list")
        data = {"email": "test5@example.com", "password": "12345"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_retrieve(self) -> None:
        """Тестирует отображение одного пользователя."""
        url = reverse("users:users-detail", args=(self.user.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["email"], self.user.email)

    def test_user_update(self) -> None:
        """Тестирует редактирование пользователя."""
        url = reverse("users:users-detail", args=(self.user.id,))
        data = {"email": "test3@example.com"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["email"], "test3@example.com")

    def test_user_delete(self) -> None:
        """Тестирует удаление пользователя."""
        url = reverse("users:users-detail", args=(self.user.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self) -> None:
        """Тестирует вывод списка пользователей."""
        url = reverse("users:users-list")
        response = self.client.get(url)
        data = response.json()
        result = [{"id": self.user.id, "town": None, "avatar": None}]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
