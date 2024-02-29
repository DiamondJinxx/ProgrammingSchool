from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from auto.api.serializers import (
    VehicleSerializer,
    DriverSerializer,
    EnterpriseSerializer
)

from auto.models import (
    Driver,
    Enterprise,
    Manager,
    Vehicle, 
)
from auto.permissions import IsSameEnterprise, IsManager


def filter_by_manager_enterprise(queryset, request, enterprise_id=False):
    if request.user.is_superuser:
        return queryset
    manager = Manager.objects.get(user_id=request.user.id)
    if enterprise_id:
        queryset = queryset.filter(id__in=manager.enterprises.all())
    else:
        queryset = queryset.filter(enterprise__in=manager.enterprises.all())
    return queryset


@method_decorator(csrf_protect, name='dispatch')
class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated, IsManager, IsSameEnterprise]

    def list(self, request, *args, **kwargs):
        self.queryset = filter_by_manager_enterprise(self.queryset, request)
        return super().list(request, *args, **kwargs)


@method_decorator(csrf_protect, name='dispatch')
class DriversViewSet(ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    permission_classes = [IsAuthenticated, IsManager, IsSameEnterprise]

    def list(self, request, *args, **kwargs):
        self.queryset = filter_by_manager_enterprise(self.queryset, request)
        return super().list(request, *args, **kwargs)


@method_decorator(csrf_protect, name='dispatch')
class EnterpriseViewSet(ModelViewSet):
    serializer_class = EnterpriseSerializer
    queryset = Enterprise.objects.all()
    permission_classes = [IsAuthenticated, IsManager]

    def list(self, request, *args, **kwargs):
        self.queryset = filter_by_manager_enterprise(self.queryset, request, enterprise_id=True)
        return super().list(request, *args, **kwargs)

