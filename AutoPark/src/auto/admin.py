from django.contrib import admin
from auto.models import Vehicle, VehicleType, Brand

# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'mileage', 'release_year', 'brand']


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'load_capacity', 'number_of_seats', 'fuel_capacity', 'max_speed', 'vehicle_type']
