from rest_framework.viewsets import ModelViewSet
from auto.api.serializers import (
    VehicleSerializer,
    DriverSerializer,
    EnterpriseSerializer
)

from auto.models import (
    Enterprise,
    Vehicle, 
    Driver
)


class VehicleViewSet(ModelViewSet):
    serializer_class=VehicleSerializer
    queryset=Vehicle.objects.all()


class DriversViewSet(ModelViewSet):
    serializer_class=DriverSerializer
    queryset=Driver.objects.all()


class EnterpriseViewSet(ModelViewSet):
    serializer_class=EnterpriseSerializer
    queryset=Enterprise.objects.all()


