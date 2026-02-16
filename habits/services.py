import logging
from typing import Any

import requests

from crswrk_5.settings import TELEGRAM_TOKEN, TELEGRAM_URL

logger = logging.getLogger(__name__)


def send_telegram_reminder(chat_id: Any, message: str) -> None:
    """Отправляет сообщение в телеграм чат"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    try:
        response = requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при отправке сообщения в Telegram (chat_id: {chat_id}): {e}")
