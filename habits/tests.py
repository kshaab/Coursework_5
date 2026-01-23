from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование эндпоинтов привычки"""

    def setUp(self) -> None:
        """Создает тестовую привычку у пользователя"""
        self.user = User(email="test@example.com")
        self.user.set_password("12345")
        self.user.save()
        self.habit = Habit.objects.create(
            action="Прогулка",
            user=self.user,
            place="Парк",
            time=datetime.now().time(),
            duration=60,
            periodicity=1,
            reward="Ванна с пеной",
            is_public=True,
            is_pleasant=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self) -> None:
        """Тестирует создание привычки"""
        url = reverse("habits:habit-create")
        data = {
            "action": "Прогулка",
            "user": self.user.id,
            "place": "Сквер",
            "time": datetime.now().strftime("%H:%M"),
            "duration": 60,
            "periodicity": 1,
            "reward": "Ванна с пеной",
            "is_public": True,
            "is_pleasant": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habits_list(self) -> None:
        """Тестирует вывод списка привычек"""
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "place": self.habit.place,
                    "time": self.habit.time.isoformat(),
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "periodicity": self.habit.periodicity,
                    "reward": self.habit.reward,
                    "duration": self.habit.duration,
                    "is_public": self.habit.is_public,
                    "user": self.habit.user.id,
                    "related_habit": self.habit.related_habit_id,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self) -> None:
        """Тестирует отображение одной привычки"""
        url = reverse("habits:habit-retrieve", args=(self.habit.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["action"], self.habit.action)

    def test_habit_update(self) -> None:
        """Тестирует редактирование привычки"""
        url = reverse("habits:habit-update", args=(self.habit.id,))
        data = {
            "place": "Лес",
            "reward": self.habit.reward,
            "duration": self.habit.duration,
            "periodicity": self.habit.periodicity,
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["place"], "Лес")

    def test_habit_delete(self) -> None:
        """Тестирует удаление привычки"""
        url = reverse("habits:habit-delete", args=(self.habit.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
