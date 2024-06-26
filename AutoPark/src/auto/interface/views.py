import datetime
from django.shortcuts import get_object_or_404, redirect
from auto import models
from auto.api.serializers import VehicleSerializer, GeotagSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.settings import env


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
        queryset = models.Vehicle.objects.filter(enterprise_id=enterprise_id)
        return Response({'vehicles': queryset})


class UserVehicleDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vehicle_detail.html'

    def get(self, request, enterprise_id, vehicle_id):
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        serializer = VehicleSerializer(vehicle)
        trips = models.Trip.objects.filter(vehicle__id=vehicle.id)
        vehicle.orm_trips = trips
        return Response({'serializer': serializer, 'vehicle': vehicle})

    def post(self, request, enterprise_id, vehicle_id):
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'vehicle': vehicle})
        serializer.save()
        return redirect('user-vehicle-list', enterprise_id=enterprise_id)


class UserVehicleCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vehicle_create.html'

    def get(self, request, enterprise_id):
        vehicle = models.Vehicle()
        vehicle.enterprise_id = enterprise_id
        serializer = VehicleSerializer(vehicle)
        return Response({'serializer': serializer, 'vehicle': vehicle})

    def post(self, request, enterprise_id):
        vehicle = models.Vehicle()
        vehicle.enterprise_id = enterprise_id
        serializer = VehicleSerializer(vehicle, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'vehicle': vehicle})
        serializer.save()
        return redirect('user-vehicle-list', enterprise_id=enterprise_id)


class UserVehicleDelete(APIView):

    def get(self, request, enterprise_id, vehicle_id):
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
        time_from = self.request.query_params.get('time_from')
        time_to = self.request.query_params.get('time_to')
        if not time_from or not time_to:
            return Response({
                "trips": [],
                "time_from": '',
                "time_to": '',
            })
        time_from = datetime.datetime.fromisoformat(time_from)
        time_to = datetime.datetime.fromisoformat(time_to)
        vehicle = get_object_or_404(models.Vehicle, pk=vehicle_id)
        trips = models.Trip.objects.filter(
            vehicle__id=vehicle.id,
            start_date__gte=set_utc(time_from),
            end_date__lte=set_utc(time_to),
        )
        for trip in trips:
            points = models.Geotag.objects.filter(
                timestamp__gte=set_utc(trip.start_date),
                timestamp__lte=set_utc(trip.end_date),
                vehicle__id=vehicle.id,
            ).order_by('timestamp')
            points_data = list(map(lambda tag: tag["point"]["coordinates"], GeotagSerializer(points, many=True).data))
            trip.points = points_data
        return Response({
            'trips': trips,
            "time_from": str(time_from),
            "time_to": str(time_to),
            "map_api_key": env("GEODECODER_API_KEY"),
        })


class UserReportsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reports_list.html'

    def get(self, request, enterprise_id, vehicle_id):
        time_from = self.request.query_params.get('time_from')
        time_to = self.request.query_params.get('time_to')
        report_period = self.request.query_params.get('report_period')
        if not time_from or not time_to or not report_period:
            return Response({
                "reports": [],
                "types": {report_type.value: report_type.name for report_type in models.AbstractReport.PeriodType},
                "type_mapper": {
                    models.AbstractReport.PeriodType.DAY: "По дням",
                    models.AbstractReport.PeriodType.MONTH: "По месяцам",
                    models.AbstractReport.PeriodType.HALF_YEAR: "По полугодиям",
                },
                "start_date": '',
                "end_date": '',
            })
        time_from = datetime.datetime.fromisoformat(time_from)
        time_to = datetime.datetime.fromisoformat(time_to)
        type_to_strategy_mapper = {
            models.AbstractReport.PeriodType.DAY: "По дням",
        },

        reports = models.MileageReport.objects.filter(
            start_date__gte=set_utc(time_from),
            end_date__lte=set_utc(time_to),
            vehicle__id=vehicle_id,
            period=str(report_period),
        )
        print(reports.query)
        return Response({
            "reports": reports,
            "types": {report_type.value: report_type.name for report_type in models.AbstractReport.PeriodType},
            "type_mapper": {
                models.AbstractReport.PeriodType.DAY: "По дням",
                models.AbstractReport.PeriodType.MONTH: "По месяцам",
                models.AbstractReport.PeriodType.HALF_YEAR: "По полугодиям",
            },
            "start_date": str(time_from),
            "end_date": str(time_to),
        })


class UserReportsMileageDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reports_mileage_detail.html'

    def get(self, request, enterprise_id, vehicle_id, report_id):
        report = models.MileageReport.objects.get(id=report_id)
        return Response({
            "report": report,
        })
