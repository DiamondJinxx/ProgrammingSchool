from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from auto.models import Manager


class UserIsNotManager(APIException):
    status_code = 401
    default_detail = "Current user is not a Manager"
    default_code = "user_is_not_manager"


class IsManager(BasePermission):
    """Проверка, что авторизованный пользователь является менеджером."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            manager = Manager.objects.get(user_id=request.user.id)
        except Manager.DoesNotExist:
            raise UserIsNotManager()
        return bool(manager)

