from rest_framework.routers import SimpleRouter
from django.urls import path, include
from auto.api.views import (
    VehicleViewSet,
    DriversViewSet,
    EnterpriseViewSet,
    GeotagViewSet,
)


router = SimpleRouter()
router.register('/vehicles', VehicleViewSet)
router.register('/vehicles/(?P<vehicle_id>.+)/geotags', GeotagViewSet)
router.register('/enterprises', EnterpriseViewSet)
router.register('/drivers', DriversViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
