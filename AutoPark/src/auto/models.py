from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    price = models.IntegerField()
    mileage = models.IntegerField()
    release_year = models.IntegerField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    time_of_purchase = models.DateTimeField()
    enterprise = models.ForeignKey(
        'Enterprise',
        on_delete=models.SET_NULL,
        null=True,
        related_name='vehicles'
    )
    drivers = models.ManyToManyField(
        'Driver',
        related_name='vehicles',
    )
    active_driver = models.OneToOneField(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='active_vehicle'
    )

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

    def clean(self):
        old_object = Vehicle.objects.get(id=self.id)
        if self.active_driver and self.enterprise != old_object.enterprise:
            raise ValidationError('Нельзя обновить предприятие у ТС с активным водителем!')

    def __str__(self):
        return f"{self.id}: {str(self.brand)} - {self.release_year}"

    def stringify(self):
        return str(self)

    def link_to_delete(self):
        return f"{self.id}/delete"


class VehicleType(models.Model):
    description = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Тип транспортного средства"
        verbose_name_plural = "Типы транспортных средст"

    def __str__(self):
        return self.description


class Brand(models.Model):
    name = models.CharField(max_length=40)
    load_capacity = models.DecimalField(max_digits=4, decimal_places=2)
    number_of_seats = models.IntegerField() 
    fuel_capacity = models.IntegerField()
    max_speed = models.IntegerField()
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Автомобильный бренд"
        verbose_name_plural = "Автомобильные бренды"

    def __str__(self):
        return f"{self.name}: {self.vehicle_type.description}"

    # def __int__(self):
    #     return self.id


class Enterprise(models.Model):
    """Модель предприятия"""
    TIMEZONES = tuple(zip(timezone.zoneinfo.available_timezones(), timezone.zoneinfo.available_timezones()))
    name = models.CharField(max_length=240)
    city = models.CharField(max_length=3)
    foundation_date = models.DateField()
    time_zone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"

    def __str__(self):
        return f"{self.name}({self.foundation_date})"

    def vehicles_list_url(self):
        return f"{self.id}/vehicles"


class Driver(models.Model):
    """Водитель"""
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=40, blank=False)
    salary = models.IntegerField()
    enterprise = models.ForeignKey(
        Enterprise, 
        on_delete=models.SET_NULL, 
        related_name='drivers',
        null=True
    )

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.patronymic}"


class Manager(models.Model):
    """Менеджер. Может авторизоваться в админке."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprises = models.ManyToManyField(
        Enterprise,
        related_name='managers'
    )

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"

    def __str__(self):
        return self.user.username


class Geotag(models.Model):
    """ Точка для трека."""
    point = gis_models.PointField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='geotags')
    timestamp = models.DateTimeField()


class Trip(models.Model):
    """Поездка автомобиля."""

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
