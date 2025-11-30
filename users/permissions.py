from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Класс доступов для владельцев"""

    def has_object_permission(self, request, view, obj):
        """Метод проверки принадлежности записи пользователю"""

        return obj.owner == request.user


class IsOwnerOrPublic(permissions.BasePermission):
    """Класс доступов для владельцев или по наличию флага публичности"""

    def has_object_permission(self, request, view, obj):
        """Метод проверки принадлежности записи пользователю или наличию у записи флага публичности"""

        return (obj.owner == request.user) or (obj.is_public)
