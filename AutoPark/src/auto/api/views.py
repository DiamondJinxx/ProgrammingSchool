from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
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


def filter_by_manager_enterprise(queryset, request, enterprise_id=False):
    if request.user.is_superuser:
        return queryset
    manager = Manager.objects.get(user_id=request.user.id)
    if enterprise_id:
        queryset = queryset.filter(id__in=manager.enterprises.all())
    else:
        queryset = queryset.filter(enterprise__in=manager.enterprises.all())
    return queryset


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                    'message': 'You are not authorized to access this resource.', 
                    'status_code': 401
                }

            return JsonResponse(
                data,
                status=401
            )
        self.queryset = filter_by_manager_enterprise(self.queryset, request)
        return super().list(request, *args, **kwargs)


class DriversViewSet(ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                    'message': 'You are not authorized to access this resource.', 
                    'status_code': 401
                }

            return JsonResponse(
                data,
                status=401
            )
        self.queryset = filter_by_manager_enterprise(self.queryset, request)
        return super().list(request, *args, **kwargs)



class EnterpriseViewSet(ModelViewSet):
    serializer_class = EnterpriseSerializer
    queryset = Enterprise.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            data = {
                    'message': 'You are not authorized to access this resource.', 
                    'status_code': 401
                }

            return JsonResponse(
                data,
                status=401
            )
        self.queryset = filter_by_manager_enterprise(self.queryset, request, enterprise_id=True)
        return super().list(request, *args, **kwargs)

