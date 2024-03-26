from django.urls import path
from auto.interface.views import (
    UserEnterprisesList,
    UserVehiclesList,
    UserVehicleDetail,
)

urlpatterns = [
    path(
        'enterprises/',
        UserEnterprisesList.as_view(template_name='enterprise_list.html'),
        name='user-enterprises-list'
    ),
    path(
        'enterprises/<int:enterprise_id>/vehicles/',
        UserVehiclesList.as_view(template_name='vehicle_list.html'),
        name='user-vehicle-list'
    ),
    path(
        'enterprises/<int:enterprise_id>/vehicles/<int:vehicle_id>/',
        UserVehicleDetail.as_view(template_name='vehicle_detail.html'),
        name='user-vehicle-detail'
    ),
]
