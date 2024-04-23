import datetime

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from auto.api.serializers import (
    VehicleSerializer,
    DriverSerializer,
    EnterpriseSerializer,
    GeotagSerializer,
    GeotagGeoJsonSerializer,
)

from auto.models import (
    Driver,
    Enterprise,
    Manager,
    Vehicle,
    Geotag,
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


@method_decorator(csrf_protect, name='dispatch')
class GeotagViewSet(ModelViewSet):
    queryset = Geotag.objects.all()
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if not vehicle_id:
            raise
        time_from = self.request.query_params.get('time_from')
        time_to = self.request.query_params.get('time_to')
        tags = Geotag.objects.filter(vehicle=vehicle_id)
        if time_from:
            time_from = datetime.datetime.fromisoformat(time_from)
            time_from = self.set_utc(time_from)
            tags = tags.filter(timestamp__gt=time_from)
        if time_to:
            time_to = self.set_utc(time_to)
            tags = tags.filter(timestamp__lt=time_to)
        tags = tags.order_by("-timestamp")
        return tags

    def get_serializer_class(self, *args, **kwargs):
        geo_json = self.request.query_params.get('geoJson')
        return GeotagGeoJsonSerializer if geo_json else GeotagSerializer

    @staticmethod
    def set_utc(time_from: datetime.datetime):
        """Set utc time to datetime"""
        return datetime.datetime(
            time_from.year,
            time_from.month,
            time_from.day,
            time_from.hour,
            time_from.minute,
            time_from.second,
            tzinfo=datetime.timezone.utc
        )
