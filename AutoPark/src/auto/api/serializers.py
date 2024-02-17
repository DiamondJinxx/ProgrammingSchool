from rest_framework import serializers
from auto.models import Brand, Vehicle, VehicleType, Enterprise, Driver


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
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    enterprise_id = serializers.PrimaryKeyRelatedField(queryset=Enterprise.objects.all())

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'price',
            'mileage',
            'release_year',
            'brand_id',
            'enterprise_id',
            'active_driver',
            'drivers'
        ]


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
