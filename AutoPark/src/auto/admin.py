from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from auto.models import (
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
        'brand',
        'enterprise',
        'active_driver'
    ]

    @admin.display()
    def active_driver(self, vehicle: Vehicle):
        return str(vehicle.active_driver)


    # def save_model(self, request, obj, form, change):
        # if obj.active_driver and form['enterprise'] != obj.enterprise:
        #     messages.add_message(
        #         request,
        #         messages.ERROR,
        #         "Нельзя изменить предприятие ТС при наличии активного водителя"
        #     )
        #     return
        # return super().save_model(request, obj, form, change)


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
    ]


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
