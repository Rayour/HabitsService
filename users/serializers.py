from rest_framework import serializers

from users.models import CustomUser, Habit


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = CustomUser
        fields = ("id", "email", "phone_number", "tg_chat_id", "username", "password")


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычки"""

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        """Проверка корректности объекта привычки"""

        # У приятной привычки не может быть вознаграждения или связанной привычки.
        if data["is_enjoyable"] and (data["related_habit"] or data["reward"]):
            raise serializers.ValidationError(
                {"reward": "У приятной привычки не может быть указано вознаграждение или привычка-вознаграждение"}
            )

        # Исключить одновременный выбор связанной привычки и указания вознаграждения.
        if data["related_habit"] and data["reward"]:
            raise serializers.ValidationError(
                {"reward": "Нельзя одновременно указывать и вознаграждение и приятную привычку для вознаграждения"}
            )

        # Время выполнения должно быть не больше 120 секунд.
        if data["duration"] > 120:
            raise serializers.ValidationError({"duration": "Время выполнения привычки не должно превышать 120 секунд"})

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.

        if data["related_habit"]:
            related_habit = data["related_habit"]
            if not related_habit or not related_habit.is_enjoyable:
                raise serializers.ValidationError(
                    {"related_habit": "В качестве привычки-вознаграждения можно указать только приятную привычку"}
                )

        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        if data["period_in_days"] > 7:
            raise serializers.ValidationError(
                {"period_in_days": "Период выполнения привычки не может превышать 7 дней"}
            )

        return data
