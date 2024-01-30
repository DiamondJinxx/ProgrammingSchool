from django.db import models

# Create your models here.

class Vehicle(models.Model):
    price = models.IntegerField()
    mileage = models.IntegerField()
    release_year = models.IntegerField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"


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
