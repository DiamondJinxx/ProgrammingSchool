import datetime
from pprint import pprint
from django.shortcuts import get_object_or_404, redirect
from auto import models
from auto.api.serializers import VehicleSerializer, GeotagSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserEnterprisesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'enterprise_list.html'

    def get(self, request):
        manager = models.Manager.objects.get(user_id=request.user.id)
        queryset = models.Enterprise.objects.filter(id__in=manager.enterprises.all())
        return Response({'enterprises': queryset})


class UserVehiclesList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vehicle_list.html'

    def get(self, request, enterprise_id: int):
        print(self.kwargs)
        # queryset = models.Vehicle.objects.filter(id__in=manager.enterprises.all())
        queryset = models.Vehicle.objects.filter(enterprise_id=enterprise_id)
        return Response({'vehicles': queryset})


class UserVehicleDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vehicle_detail.html'

    def get(self, request, enterprise_id, vehicle_id):
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        serializer = VehicleSerializer(vehicle)
        print(serializer.data)
        trips = models.Trip.objects.filter(vehicle__id=vehicle.id)
        vehicle.orm_trips = trips
        return Response({'serializer': serializer, 'vehicle': vehicle})

    def post(self, request, enterprise_id, vehicle_id):
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'vehicle': vehicle})
        print('before save')
        serializer.save()
        return redirect('user-vehicle-list', enterprise_id=enterprise_id)


class UserVehicleCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vehicle_create.html'

    def get(self, request, enterprise_id):
        print(f'enterprise is {enterprise_id}')
        vehicle = models.Vehicle()
        vehicle.enterprise_id = enterprise_id
        serializer = VehicleSerializer(vehicle)
        return Response({'serializer': serializer, 'vehicle': vehicle})

    def post(self, request, enterprise_id):
        # print('post method')
        # print(f'enerprise {enterprise_id}')
        # print(f'vehicle {vehicle_id}')
        # print(f'request_data {request.data}')
        vehicle = models.Vehicle()
        vehicle.enterprise_id = enterprise_id
        serializer = VehicleSerializer(vehicle, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'vehicle': vehicle})
        print('before save')
        serializer.save()
        return redirect('user-vehicle-list', enterprise_id=enterprise_id)


class UserVehicleDelete(APIView):

    def get(self, request, enterprise_id, vehicle_id):
        print('vehicle was deleted')
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        vehicle.delete()
        return redirect('user-vehicle-list', enterprise_id=enterprise_id)


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


class UserTripsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'trips_list.html'

    def get(self, request, enterprise_id, vehicle_id):
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        trips = models.Trip.objects.filter(vehicle__id=vehicle.id)
        t = 0
        for trip in trips:
            points = models.Geotag.objects.filter(
                timestamp__gte=set_utc(trip.start_date),
                timestamp__lte=set_utc(trip.end_date),
            ).order_by('timestamp')
            points_data = list(map(lambda tag: tag["point"]["coordinates"], GeotagSerializer(points, many=True).data))
            if t != 0:
                trip.points = []
                continue
            t += 1
            pprint(points_data)
            trip.points = points_data
        return Response({'trips': trips})
