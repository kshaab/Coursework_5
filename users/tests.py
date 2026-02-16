import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

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

        expected = [{"id": self.user.id, "town": None, "avatar": None}]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["results"], expected)
        self.assertEqual(data["count"], 1)
        self.assertIsNone(data["next"])
        self.assertIsNone(data["previous"])


@pytest.mark.django_db
class TestUserPagination:
    """Тестирование пагинации пользователей"""

    def setup_method(self) -> None:
        """Создает пользователя и список из 12 пользователей"""
        self.client = APIClient()
        self.url = reverse("users:users-list")

        self.users = []
        for i in range(12):
            user = User.objects.create(
                email=f"user{i}@test.com",
                is_staff=False,
                is_superuser=False,
            )
            user.set_password("testpass123")
            user.save()
            self.users.append(user)

        self.client.force_authenticate(user=self.users[0])

    def test_default_page_size(self) -> None:
        """Тестирует количество пользователей на странице"""
        response = self.client.get(self.url)
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 5

    def test_second_page(self) -> None:
        """Тестирует количество пользователей на второй странице"""
        response = self.client.get(f"{self.url}?page=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 5

    def test_last_page(self) -> None:
        """Тестирует количество пользователей на последней странице"""
        response = self.client.get(f"{self.url}?page=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2

    def test_custom_page_size(self) -> None:
        """Тестирует изменение количества пользователей на странице через URL"""
        response = self.client.get(f"{self.url}?page_size=7")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 7

    def test_max_page_size(self) -> None:
        """Тестирует максимальное количество пользователей на странице"""
        response = self.client.get(f"{self.url}?page_size=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 10  # max_page_size = 10
