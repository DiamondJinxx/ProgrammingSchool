from rest_framework import serializers
from auto.models import Brand, Vehicle, VehicleType


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = [
            'id',
            'description',
        ]


class BrandSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleTypeSerializer()
    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'load_capacity',
            'number_of_seats',
            'fuel_capacity',
            'max_speed',
            'vehicle_type'
        ]


class VehicleSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'price',
            'mileage',
            'release_year',
            'brand'
        ]

