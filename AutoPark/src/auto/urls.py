from rest_framework.routers import SimpleRouter
from django.urls import path, include
from auto.api.views import VehicleViewSet


router = SimpleRouter()
router.register('', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
