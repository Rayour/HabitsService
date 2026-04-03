from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser, Habit


class HabitTestCase(APITestCase):
    """Класс для тестирования CRUD привычки"""

    def setUp(self):
        """Метод создания тестовых данных"""

        self.user = CustomUser.objects.create(email="test@test.ru", username="test", password="111")
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Место",
            time="12:00:00",
            action="Действие_полезное",
            related_habit=None,
            is_enjoyable=False,
            period_in_days=1,
            reward="Вознаграждение",
            duration=90,
            is_public=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        """Метод для проверки просмотра привычки"""
        url = reverse("users:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        """Метод для проверки создания привычки"""

        url = reverse("users:habit_create")
        data = {
            "place": "Место2",
            "time": "12:00:00",
            "action": "Действие2_полезное",
            "is_enjoyable": False,
            "period_in_days": 1,
            "reward": "Вознаграждение2",
            "duration": 90,
            "is_public": True,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Метод для проверки обновления привычки"""

        url = reverse("users:habit_update", args=(self.habit.pk,))
        data = {
            "action": "Действие11",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Действие11")

    def test_habit_delete(self):
        """Метод для проверки удаления привычки"""

        url = reverse("users:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_own_list(self):
        """Метод для проверки списка собственных привычек"""

        url = reverse("users:habits_own_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)
        self.assertEqual(data["results"][0]["id"], self.habit.pk)
        self.assertEqual(data["results"][0]["owner"], self.user.pk)
        self.assertEqual(data["results"][0]["place"], self.habit.place)
        self.assertEqual(data["results"][0]["time"], self.habit.time)
        self.assertEqual(data["results"][0]["action"], self.habit.action)
        self.assertEqual(data["results"][0]["is_enjoyable"], self.habit.is_enjoyable)
        self.assertEqual(data["results"][0]["period_in_days"], self.habit.period_in_days)
        self.assertEqual(data["results"][0]["reward"], self.habit.reward)
        self.assertEqual(data["results"][0]["duration"], self.habit.duration)
        self.assertEqual(data["results"][0]["is_public"], self.habit.is_public)

    def test_habit_public_list(self):
        """Метод для проверки списка публичных привычек"""

        url = reverse("users:habits_public_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["next"], None)
        self.assertEqual(data["previous"], None)


class CustomUserTestCase(APITestCase):
    """Класс для тестирования CRUD пользователя"""

    def setUp(self):
        """Метод создания тестовых данных"""

        self.user = CustomUser.objects.create(email="test@test.ru", username="test", password="111")
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        """Метод для проверки просмотра пользователя"""
        url = reverse("users:users_retrieve", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        """Метод для проверки создания пользователя"""

        url = reverse("users:users_create")
        data = {
            "email": "test2@mail.ru",
            "username": "test2",
            "password": "222",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.all().count(), 2)

    def test_user_update(self):
        """Метод для проверки обновления пользователя"""

        url = reverse("users:users_update", args=(self.user.pk,))
        data = {
            "tg_chat_id": "123",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("tg_chat_id"), "123")

    def test_user_delete(self):
        """Метод для проверки удаления пользователя"""

        url = reverse("users:users_delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.all().count(), 0)

    def test_user_list(self):
        """Метод для проверки списка пользователей"""

        url = reverse("users:users_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["username"], self.user.username)
        self.assertEqual(data[0]["email"], self.user.email)
