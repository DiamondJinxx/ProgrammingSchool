from django.urls import path, include

urlpatterns = [
    path('v1/auto', include('auto.urls'))
]
