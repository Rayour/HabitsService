from datetime import timedelta

import pytz
from celery import shared_task
from django.utils import timezone

from config.settings import REMIND_TIMEDELTA, TIME_ZONE
from users.models import Habit
from users.servises import send_tg_notification


@shared_task
def habits_notification():
    """Функция выбора привычек для отправки уведомлений в телеграм"""

    utc_now = timezone.now()
    utc_plus_3_timezone = pytz.timezone(TIME_ZONE)
    current_date_time = utc_now.astimezone(utc_plus_3_timezone)

    time_to_remind_start = (current_date_time + timedelta(minutes=REMIND_TIMEDELTA)).time()
    time_to_remind_stop = (current_date_time + timedelta(minutes=(REMIND_TIMEDELTA + 1))).time()

    habits_to_remind = Habit.objects.filter(time__gte=time_to_remind_start, time__lt=time_to_remind_stop)

    for habit in habits_to_remind:
        chat_id = habit.owner.tg_chat_id
        rewarding = habit.reward if habit.reward else habit.related_habit.action
        message = f"Через {REMIND_TIMEDELTA} минут пора выполнить {habit.action.lower()} \
и получить в награду {rewarding.lower()}"
        send_tg_notification(chat_id, message)
