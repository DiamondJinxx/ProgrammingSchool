from rest_framework.routers import SimpleRouter
from django.urls import path, include
from auto.api.views import VehicleViewSet, DriversViewSet, EnterpriseViewSet


router = SimpleRouter()
router.register('/vehicles', VehicleViewSet)
router.register('/enterprise', EnterpriseViewSet)
router.register('/drivers', DriversViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
