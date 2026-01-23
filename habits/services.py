from typing import Any

import requests

from crswrk_5.settings import TELEGRAM_TOKEN, TELEGRAM_URL


def send_telegram_reminder(chat_id: Any, message: str) -> None:
    """Отправляет сообщение в телеграм чат"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
