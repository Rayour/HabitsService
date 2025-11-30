from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Habit
from users.permissions import IsOwner, IsOwnerOrPublic
from users.serializers import CustomUserSerializer, HabitSerializer


class CustomUserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод создания кастомного юзера с хешированием пароля"""

        user = serializer.save()
        user.set_password(user.password)
        user.save()


class CustomUserUpdateAPIView(UpdateAPIView):
    """Обновление пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsOwner,)


class CustomUserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsOwner,)


class CustomUserRetrieveAPIView(RetrieveAPIView):
    """Получение пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsOwner,)


class CustomUserListAPIView(ListAPIView):
    """Получение списка пользователей"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class HabitCreateAPIView(CreateAPIView):
    """Создание привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Метод создания с сохранением пользователя в качестве владельца"""
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitUpdateAPIView(UpdateAPIView):
    """Обновление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(DestroyAPIView):
    """Удаление привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Получение привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwnerOrPublic,)


class HabitListAPIView(ListAPIView):
    """Получение списка привычек"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        """Метод получения доступных для просмотра привычек"""

        user = self.request.user
        user_own_habits = Habit.objects.filter(owner=user)
        public_habits = Habit.objects.filter(is_public=True)
        return user_own_habits.union(public_habits)
