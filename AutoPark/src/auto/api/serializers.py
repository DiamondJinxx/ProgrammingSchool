from django.utils import timezone
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from auto.models import (
    Brand,
    Vehicle,
    VehicleType,
    Enterprise,
    Driver,
    Geotag,
)


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = [
            'id',
            'description',
        ]


class BrandSerializer(serializers.ModelSerializer):
    vehicle_type_id = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'load_capacity',
            'number_of_seats',
            'fuel_capacity',
            'max_speed',
            'vehicle_type_id'
        ]


class VehicleSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source="brand")
    enterprise_id = serializers.PrimaryKeyRelatedField(
        queryset=Enterprise.objects.all(),
        source="enterprise",
        allow_null=True
    )
    drivers = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        many=True,
        allow_null=True,
    )

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'price',
            'mileage',
            'release_year',
            # 'time_of_purchase',
            'brand_id',
            'enterprise_id',
            'active_driver',
            'drivers'
        ]

    def to_representation(self, instance):
        tz = timezone.zoneinfo.ZoneInfo(instance.enterprise.time_zone)
        self.fields['time_of_purchase'] = serializers.DateTimeField(
            default_timezone=tz,
            # initial=lambda: instance.time_of_purchase.strftime("%%Y-%%m-%%d %%H:%%M")
        )
        return super().to_representation(instance)


class EnterpriseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enterprise
        fields = [
            'name',
            'city',
            'foundation_date',
            'vehicles',
            'drivers'
        ]


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = [
            'first_name',
            'second_name',
            'patronymic',
            'salary',
            'enterprise'
        ]


class GeotagSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source="vehicle",
    )

    class Meta:
        model = Geotag
        fields = [
            'vehicle_id',
            'timestamp',
            'point'
        ]

    def to_representation(self, instance):
        tz = timezone.zoneinfo.ZoneInfo(instance.vehicle.enterprise.time_zone)
        self.fields['timestamp'] = serializers.DateTimeField(
            default_timezone=tz,
            # initial=lambda: instance.time_of_purchase.strftime("%%Y-%%m-%%d %%H:%%M")
        )
        return super().to_representation(instance)


class GeotagGeoJsonSerializer(GeoFeatureModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source="vehicle",
    )

    class Meta:
        model = Geotag
        geo_field = "point"
        fields = [
            'vehicle_id',
            'timestamp',
            'point'
        ]

    def to_representation(self, instance):
        tz = timezone.zoneinfo.ZoneInfo(instance.vehicle.enterprise.time_zone)
        self.fields['timestamp'] = serializers.DateTimeField(
            default_timezone=tz,
            # initial=lambda: instance.time_of_purchase.strftime("%%Y-%%m-%%d %%H:%%M")
        )
        return super().to_representation(instance)
