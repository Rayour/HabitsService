import requests

from config.settings import TG_BOT_TOKEN, TG_URL


def send_tg_notification(chat_id, message):
    """Функция отправки уведомлеий в телеграм"""

    url = f"{TG_URL}/bot{TG_BOT_TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": message}

    requests.get(url, params=params)
