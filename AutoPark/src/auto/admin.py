from django.contrib import admin
from auto.models import Vehicle

# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'mileage', 'release_year']

