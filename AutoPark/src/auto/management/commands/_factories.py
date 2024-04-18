import factory
import random
import datetime

import auto.models as models


# TODO: делаем ручками строгую генерацию?
class VehicleTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.VehicleType

    description = factory.Faker('company')


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    name = factory.Faker("company")
    load_capacity = factory.LazyFunction(lambda: random.random() * random.randint(5, 10))
    number_of_seats = factory.LazyFunction(lambda: random.randint(2, 6)) 
    fuel_capacity = factory.LazyFunction(lambda: random.randint(16, 64))
    max_speed = factory.LazyFunction(lambda: random.randint(160, 280))
    vehicle_type = factory.SubFactory(VehicleTypeFactory)


_CITY_CODES = ["МСК", "ЕКБ", "СПБ", "НСБ", "КЗН",]
class EnterpriseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Enterprise

    name = factory.Faker("company")
    city = factory.LazyFunction(lambda: _CITY_CODES[random.randint(0, len(_CITY_CODES) - 1)])
    foundation_date = factory.Faker("date_between")


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Driver

    first_name = factory.Faker('first_name', locale='ru_RU')
    second_name = factory.Faker('last_name', locale="ru_RU")
    patronymic = factory.Faker('middle_name', locale='ru_RU')
    salary = factory.LazyFunction(lambda: random.randint(10000, 100000))
    enterprise = None


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vehicle

    price = factory.LazyFunction(lambda: random.randint(10000, 100000))
    mileage = factory.LazyFunction(lambda: random.randint(10000, 100000))
    release_year = factory.LazyFunction(lambda: random.randint(1960, 2024))
    brand = factory.SubFactory(BrandFactory)
    time_of_purchase = factory.LazyFunction(datetime.datetime.utcnow)
    enterprise = None
    active_driver = None

    @factory.post_generation
    def drivers(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.drivers.add(*extracted)


