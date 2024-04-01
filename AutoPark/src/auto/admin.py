from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from auto.models import (
    Manager,
    Vehicle,
    VehicleType,
    Brand,
    Enterprise,
    Driver
)


class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        drivers = Driver.objects.filter(id=-1)
        if self.instance.enterprise:
            drivers = Driver.objects.filter(enterprise__id=self.instance.enterprise.id)
        print('type is ')
        print(self.fields)
        self.fields['drivers'].queryset = drivers
        self.fields['drivers'].required=False
        self.fields['active_driver'].queryset = drivers
        self.fields['enterprise'].required=False
        

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    form = VehicleForm
    list_display = [
        'id',
        'price',
        'mileage',
        'release_year',
        'time_of_purchase',
        'brand',
        'enterprise',
        'active_driver'
    ]

    @admin.display()
    def active_driver(self, vehicle: Vehicle):
        return str(vehicle.active_driver)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        manager = Manager.objects.get(user_id=request.user.id)
        return qs.filter(enterprise__in=manager.enterprises.all())


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'load_capacity',
        'number_of_seats',
        'fuel_capacity',
        'max_speed',
        'vehicle_type'
    ]


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'name',
    ]
    list_display = [
        'id',
        'name',
        'city',
        'foundation_date', 
        'time_zone',
    ]

    def get_queryset(self, request):
        qs = super(EnterpriseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        manager = Manager.objects.get(user_id=request.user.id)
        return qs.filter(id__in=manager.enterprises.all())

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display_links = [
        'id',
        'first_name',
        'second_name',
        'patronymic',
    ]
    list_display = [
        'id',
        'first_name',
        'second_name',
        'patronymic', 
        'salary', 
    ]

    def get_queryset(self, request):
        qs = super(DriverAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        manager = Manager.objects.get(user_id=request.user.id)
        return qs.filter(enterprise__in=manager.enterprises.all())


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    """Админка для манагера;"""
    list_display = [
        'id',
        'user',
    ]
    list_display_links = [
        'id',
        'user',
    ]

