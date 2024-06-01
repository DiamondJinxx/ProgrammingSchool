import datetime
from geopy.geocoders import Yandex

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
    TripSerializer,
    MileageReportSerializer,
)

from auto.models import (
    Driver,
    Enterprise,
    Manager,
    Vehicle,
    Geotag,
    Trip,
    MileageReport,
)
from auto.permissions import IsSameEnterprise, IsManager
from app.settings import env


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


class ModelViewUTC(ModelViewSet):
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


@method_decorator(csrf_protect, name='dispatch')
class GeotagViewSet(ModelViewUTC):
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
            time_to = datetime.datetime.fromisoformat(time_to)
            time_to = self.set_utc(time_to)
            tags = tags.filter(timestamp__lt=time_to)
        tags = tags.order_by("-timestamp")
        return tags

    def get_serializer_class(self, *args, **kwargs):
        geo_json = self.request.query_params.get('geoJson')
        return GeotagGeoJsonSerializer if geo_json else GeotagSerializer


@method_decorator(csrf_protect, name='dispatch')
class TripGeotagsViewSet(ModelViewUTC):
    queryset = Geotag.objects.all()
    serializer_class = GeotagSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if not vehicle_id:
            raise
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        trips = Trip.objects.filter(vehicle=vehicle_id)
        if date_from:
            date_from = datetime.datetime.fromisoformat(date_from)
            date_from = self.set_utc(date_from)
            trips = trips.filter(start_date__gt=date_from)
        if date_to:
            date_to = datetime.datetime.fromisoformat(date_to)
            date_to = self.set_utc(date_to)
            trips = trips.filter(end_date__lt=date_to)
        if not trips:
            # simple hack returning empty json
            return Geotag.objects.filter(id=-1)
        trips = trips.order_by("start_date")
        timestamp_from = trips.first().start_date
        timestamp_to = trips.last().end_date
        tags = Geotag.objects.filter(timestamp__gt=timestamp_from, timestamp__lt=timestamp_to)
        tags = tags.order_by("-timestamp")
        return tags


@method_decorator(csrf_protect, name='dispatch')
class TripViewSet(ModelViewUTC):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        if not vehicle_id:
            raise
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        trips = Trip.objects.filter(vehicle=vehicle_id)
        print(trips)
        if date_from:
            date_from = datetime.datetime.fromisoformat(date_from)
            date_from = self.set_utc(date_from)
            print(date_from)
            trips = trips.filter(start_date__gte=date_from)
        if date_to:
            date_to = datetime.datetime.fromisoformat(date_to)
            date_to = self.set_utc(date_to)
            print(date_to)
            trips = trips.filter(end_date__lte=date_to)
        print(trips.query)
        # if not trips:
        #     # simple hack returning empty json
        #     return Trip.objects.filter(id=-1)
        return trips

    def list(self, request, *args, **kwargs):
        responce = super().list(request, *args, **kwargs)

        geolocator = Yandex(api_key=env('GEODECODER_API_KEY'))
        for record in responce.data['results']:
            record['start_point_repr'] = self.point_representation(geolocator, record['start_point'])
            record['end_point_repr'] = self.point_representation(geolocator, record['end_point'])
        return responce

    def point_representation(self, geolocator, point) -> str:
        str_point = str(point[0]) + ', ' + str(point[1])
        location = geolocator.reverse(str_point)
        if not location:
            return "Undefined"
        return str(location)


class MileageReportViewSet(ModelViewSet):
    """Представление для отчетов по пробегу"""

    queryset = MileageReport.objects.all()
    serializer_class = MileageReportSerializer
    permission_classes = [IsAuthenticated]
