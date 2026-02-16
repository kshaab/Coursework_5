from datetime import datetime, time
from typing import Any

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch, Mock
from habits.services import send_telegram_reminder

from habits.models import Habit
from users.models import User
import pytest
from habits.validators import HabitValidator
from rest_framework.serializers import ValidationError

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

    @patch("habits.services.requests.get")
    def test_send_telegram_reminder_success(self, mock_get) -> None:
        """Тестирует успешную отправку напоминания"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        send_telegram_reminder(123, "test")

        mock_get.assert_called_once()

    def test_send_habits_reminders_task(self):
        """Покрытие Celery таска send_habits_reminders"""
    from habits.tasks import send_habits_reminders
    send_habits_reminders()

    @patch("habits.services.requests.get")
    @patch("habits.services.logger")
    def test_send_telegram_reminder_error(self, mock_logger, mock_get) -> None:
        """Тестирует вызов ошибок при отправке телеграм напоминания"""
        mock_get.side_effect = requests.exceptions.RequestException("boom")

        send_telegram_reminder(123, "test")

        mock_logger.error.assert_called_once()

    def test_owner_can_update_habit(self) -> None:
        """Тестирует возможность владельца редактировать привычку"""
        url = reverse("habits:habit-update", args=(self.habit.id,))

        data = {
            "action": self.habit.action,
            "place": "Лес",
            "time": self.habit.time.strftime("%H:%M"),
            "duration": self.habit.duration,
            "periodicity": self.habit.periodicity,
            "reward": self.habit.reward,
            "is_public": self.habit.is_public,
            "is_pleasant": self.habit.is_pleasant,
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner_cannot_update_habit(self) -> None:
        """Тестирует невозможность редактировать чужие привычки"""
        other_user = User.objects.create(email="other@test.com")
        other_user.set_password("12345")
        other_user.save()

        self.client.force_authenticate(user=other_user)

        url = reverse("habits:habit-update", args=(self.habit.id,))
        response = self.client.patch(url, {"place": "Лес"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_can_view_public_habit(self) -> None:
        """Тестирует возможность просматривать чужие публичные привычки"""
        other_user = User.objects.create(email="other@test.com")
        self.client.force_authenticate(user=other_user)

        url = reverse("habits:habit-retrieve", args=(self.habit.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_edit_public_habit(self) -> None:
        """Тестирует невозможность редактировать чужие публичные привычки"""
        other_user = User.objects.create(email="other@test.com")
        self.client.force_authenticate(user=other_user)

        url = reverse("habits:habit-update", args=(self.habit.id,))
        response = self.client.patch(url, {"place": "Море"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_any_user_can_read_profile(self) -> None:
        """Тестирует публичный просмотр профиля"""
        url = reverse("users:users-detail", args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_edit_profile(self) -> None:
        """Тестирует невозможность редактировать чужой профиль"""
        other_user = User.objects.create(email="other2@test.com")
        self.client.force_authenticate(user=other_user)

        url = reverse("users:users-detail", args=(self.user.id,))
        response = self.client.patch(url, {"email": "test@test.com"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
class TestHabitValidator:
    """Тестирование валидаторов привычек"""

    def setup_method(self) -> None:
        """Создает привычку у пользователя"""
        self.validator = HabitValidator()
        self.user = User.objects.create(email="test@test.com")

        self.pleasant_habit = Habit.objects.create(
            action="pleasant",
            user=self.user,
            is_pleasant=True,
            duration=60,
            periodicity=1,
            time=time(9, 0)
        )

    def valid_data(self) -> dict[str, Any]:
        """Устанавливает данные привычки для проверки"""
        return {
            "is_pleasant": False,
            "reward": "coffee",
            "related_habit": None,
            "duration": 60,
            "periodicity": 1,
        }


    def test_pleasant_cannot_have_reward(self) -> None:
        """Тестирует исключение одновременного выбора связанной привычки и указания вознаграждения"""
        data = self.valid_data()
        data["is_pleasant"] = True
        data["reward"] = "coffee"

        with pytest.raises(ValidationError):
            self.validator(data)

    def test_useful_must_have_reward_or_related(self) -> None:
        """Тестирует, что у привычки должно быть либо вознаграждение, либо связанная привычка"""
        data = self.valid_data()
        data["reward"] = None

        with pytest.raises(ValidationError):
            self.validator(data)


    def test_duration_gt_120(self) -> None:
        """Тестирует, что время выполнения привычки не превышает 120 сек."""
        data = self.valid_data()
        data["duration"] = 121

        with pytest.raises(ValidationError):
            self.validator(data)


    def test_related_must_be_pleasant(self) -> None:
        """Тестирует, что связанная привычка только приятная"""
        bad_habit = Habit.objects.create(
            action="bad",
            user=self.user,
            is_pleasant=False,
            duration=60,
            periodicity=1,
            time=time(9, 0)
        )

        data = self.valid_data()
        data["related_habit"] = bad_habit

        with pytest.raises(ValidationError):
            self.validator(data)


    def test_periodicity_less_than_one(self) -> None:
        """Тестирует, что привычка выполняется хотя бы 1 раз в 7 дней"""
        data = self.valid_data()
        data["periodicity"] = 0

        with pytest.raises(ValidationError):
            self.validator(data)

    def test_periodicity_more_than_seven(self) -> None:
        """Тестирует, что неделя для привычки не превышает 7 дней"""
        data = self.valid_data()
        data["periodicity"] = 8

        with pytest.raises(ValidationError):
            self.validator(data)


@pytest.mark.django_db
class TestHabitPagination:
    """Тестирование пагинации привычек"""

    def setup_method(self) -> None:
        """Создает пользователя и 12 привычек для проверки пагинации"""
        self.client = APIClient()
        self.user = User.objects.create(email="test@test.com")

        self.client.force_authenticate(user=self.user)

        for i in range(12):
            Habit.objects.create(
                user=self.user,
                action=f"Habit {i}",
                is_pleasant=False,
                duration=60,
                periodicity=1,
                time=time(9, 0),
            )

        self.url = reverse("habits:habits-list")


    def test_default_page_size(self) -> None:
        """Тестирует количество привычек на странице"""

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.data["results"]) == 5


    def test_second_page(self) -> None:
        """Тестирует количество привычек на второй странице"""

        response = self.client.get(f"{self.url}?page=2")

        assert response.status_code == 200
        assert len(response.data["results"]) == 5

    def test_last_page(self):
        """Тестирует количество привычек на последней странице"""
        response = self.client.get(f"{self.url}?page=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 2


    def test_custom_page_size(self) -> None:
        """Тестирует изменение количества привычек на странице через URL"""

        response = self.client.get(f"{self.url}?page_size=7")

        assert response.status_code == 200
        assert len(response.data["results"]) == 7


    def test_max_page_size(self) -> None:
        """Тестирует максимальное количество привычек на странице"""

        response = self.client.get(f"{self.url}?page_size=100")

        assert response.status_code == 200
        assert len(response.data["results"]) == 10




