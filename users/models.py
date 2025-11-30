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
