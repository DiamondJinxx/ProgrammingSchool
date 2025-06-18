# Наследование реализации
class HttpResponse:
    description: str
    status_code: int


class ExternServiceHttpRespoce(HttpResponse):
    service_name: str


# Льготное наследование
class Car:
    color: str
    body: str
    weight: int


class TaxiCar(Car):
    color: str = "yellow"

