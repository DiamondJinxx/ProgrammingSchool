from django.contrib import admin
from auto.models import (
    Vehicle,
    VehicleType,
    Brand,
    Enterprise,
    Driver
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'mileage', 'release_year', 'brand']


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'load_capacity', 'number_of_seats', 'fuel_capacity', 'max_speed', 'vehicle_type']


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'foundation_date']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'second_name', 'patronymic', 'salary']

