from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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

        request = self.context.get("request")
        if request and request.method == "PATCH":
            pk = self.context["request"].parser_context["kwargs"].get("pk")

            if "is_enjoyable" in data:
                is_enjoyable = data["is_enjoyable"]
            else:
                is_enjoyable = get_object_or_404(Habit, pk=pk).is_enjoyable

            if "related_habit" in data:
                related_habit = data["related_habit"]
            else:
                related_habit = get_object_or_404(Habit, pk=pk).related_habit

            if "reward" in data:
                reward = data["reward"]
            else:
                reward = get_object_or_404(Habit, pk=pk).reward
        else:
            if "is_enjoyable" in data:
                is_enjoyable = data["is_enjoyable"]
            else:
                is_enjoyable = False

            if "related_habit" in data:
                related_habit = data["related_habit"]
            else:
                related_habit = None

            if "reward" in data:
                reward = data["reward"]
            else:
                reward = None

        # У приятной привычки не может быть вознаграждения или связанной привычки.
        if is_enjoyable and (related_habit or reward):
            raise serializers.ValidationError(
                {"reward": "У приятной привычки не может быть указано вознаграждение или привычка-вознаграждение"}
            )

        # Исключить одновременный выбор связанной привычки и указания вознаграждения.
        if related_habit and reward:
            raise serializers.ValidationError(
                {"reward": "Нельзя одновременно указывать и вознаграждение и приятную привычку для вознаграждения"}
            )

        # Время выполнения должно быть не больше 120 секунд.
        if "duration" in data and data["duration"] > 120:
            raise serializers.ValidationError({"duration": "Время выполнения привычки не должно превышать 120 секунд"})

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.
        if related_habit and not related_habit.is_enjoyable:
            raise serializers.ValidationError(
                {"related_habit": "В качестве привычки-вознаграждения можно указать только приятную привычку"}
            )

        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        if "period_in_days" in data and data["period_in_days"] > 7:
            raise serializers.ValidationError(
                {"period_in_days": "Период выполнения привычки не может превышать 7 дней"}
            )

        return data
