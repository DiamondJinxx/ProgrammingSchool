from rest_framework.routers import SimpleRouter
from django.urls import path, include
from auto.api.views import (
    VehicleViewSet,
    DriversViewSet,
    EnterpriseViewSet,
    GeotagViewSet,
    TripGeotagsViewSet,
    TripViewSet,
    MileageReportViewSet,
)


router = SimpleRouter()
router.register('/vehicles', VehicleViewSet)
router.register('/vehicles/(?P<vehicle_id>.+)/geotags', GeotagViewSet)
router.register('/vehicles/(?P<vehicle_id>.+)/trips/geo', TripGeotagsViewSet)
router.register('/vehicles/(?P<vehicle_id>.+)/trips', TripViewSet)
router.register('/enterprises', EnterpriseViewSet)
router.register('/drivers', DriversViewSet)
router.register('/reports', MileageReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
