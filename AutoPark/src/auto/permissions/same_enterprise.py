from rest_framework.permissions import BasePermission

from auto.models import Manager


class IsSameEnterprise(BasePermission):
    """Проверка принадлежности объекта и менеджера к одному предприятию."""

    def has_object_permission(self, request, view, obj):
        manager = Manager.objects.get(user_id=request.user.id)
        return bool(obj.enterprise in manager.enterprises.all())
