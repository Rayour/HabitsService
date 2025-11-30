from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    CustomUserCreateAPIView,
    CustomUserDestroyAPIView,
    CustomUserListAPIView,
    CustomUserRetrieveAPIView,
    CustomUserUpdateAPIView,
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("", CustomUserListAPIView.as_view(), name="users_list"),
    path("create/", CustomUserCreateAPIView.as_view(), name="users_create"),
    path("<int:pk>/update/", CustomUserUpdateAPIView.as_view(), name="users_update"),
    path("<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("<int:pk>/delete/", CustomUserDestroyAPIView.as_view(), name="users_delete"),
    path("habit/", HabitListAPIView.as_view(), name="habits_list"),
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("habit/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("habit/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit_delete"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
