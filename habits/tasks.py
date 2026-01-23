from celery import shared_task
from django.utils.timezone import now

from habits.models import Habit
from habits.services import send_telegram_reminder



@shared_task
def send_habits_reminders() -> None:
    """Отправляет пользователю напоминание о выполнении привычки в телеграм"""
    current_time = now().time()
    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute).select_related("user")
    for habit in habits:
        user = habit.user
        if not user.tg_chat_id:
            continue
        message = (f"Выполните привычку: {habit.action}\n"
                   f"Место: {habit.place}")
        send_telegram_reminder(user.tg_chat_id, message)



