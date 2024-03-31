from django.shortcuts import get_object_or_404, redirect
from auto import models
from auto.api.serializers import VehicleSerializer
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
        return Response({'serializer': serializer, 'vehicle': vehicle})

    def post(self, request, enterprise_id, vehicle_id):
        print('post method')
        print(f'enerprise {enterprise_id}')
        print(f'vehicle {vehicle_id}')
        print(f'request_data {request.data}')
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
