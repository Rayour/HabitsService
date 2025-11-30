from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser, Habit
from users.paginators import HabitCoursesPaginator
from users.permissions import IsOwner, IsOwnerOrPublic, IsSelf
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
    permission_classes = (IsSelf,)


class CustomUserDestroyAPIView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSelf,)


class CustomUserRetrieveAPIView(RetrieveAPIView):
    """Получение пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsSelf,)


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


class HabitOwnListAPIView(ListAPIView):
    """Получение списка собственных привычек пользователя"""

    serializer_class = HabitSerializer
    pagination_class = HabitCoursesPaginator

    def get_queryset(self):
        """Метод получения собственных привычек пользователя"""

        user = self.request.user
        return Habit.objects.filter(owner=user)


class HabitPublicListAPIView(ListAPIView):
    """Получение списка публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = HabitCoursesPaginator

    def get_queryset(self):
        """Метод получения публичных привычек"""

        return Habit.objects.filter(is_public=True)
