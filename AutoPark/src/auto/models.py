from django.db import models

# Create your models here.

class Vehicle(models.Model):
    price = models.IntegerField()
    mileage = models.IntegerField()
    release_year = models.IntegerField()

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"

