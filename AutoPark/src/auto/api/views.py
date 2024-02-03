from rest_framework.viewsets import ModelViewSet
from auto.api.serializers import VehicleSerializer

from auto.models import Vehicle


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()
