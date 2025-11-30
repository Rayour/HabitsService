from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="Телефон",
        help_text="Необязательное поле. Введите Ваш номер телефона",
    )
    tg_chat_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="ID чата в телеграм",
        help_text="Необязательное поле. Чтобы получать уведомления укажите Ваш ID в телеграм",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        """Строковое представление пользователя"""

        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Habit(models.Model):
    """Модель привычки"""

    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="habits",
    )
    place = models.CharField(max_length=250, verbose_name="Место выполнения привычки")
    time = models.DateTimeField(verbose_name="Время, когда необходимо выполнять привычку", blank=True, null=True)
    action = models.CharField(max_length=500, verbose_name="Действие, которое представляет собой привычка")
    is_enjoyable = models.BooleanField(verbose_name="Привычка приятная?", blank=True, null=True)
    related_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        blank=True,
        null=True,
        help_text="Укажите приятную привычку, которая будет вознаграждением",
        on_delete=models.SET_NULL,
        related_name="related_habits",
    )
    period_in_days = models.PositiveSmallIntegerField(verbose_name="Периодичность привычки в днях", default=1)
    reward = models.CharField(max_length=500, verbose_name="Действие, которое является вознаграждением")
    duration = models.PositiveSmallIntegerField(verbose_name="Продолжительность выполнения привычки в секундах")
    is_public = models.BooleanField(verbose_name="Привычка публичная?", blank=True, null=True)
