from django.core.management.base import BaseCommand, CommandError
import  random

from . import _factories as factory

class Command(BaseCommand):
    help = "Generate enterprise data"

    def add_arguments(self, parser):
        parser.add_argument("--enterprise", type=int, default=1)
        parser.add_argument("--vehicles", type=int, default=3)
        parser.add_argument("--drivers", type=int, default=5)

    def handle(self, *args, **options):
        saved_vehicles = []
        for e_id in range(options["enterprise"]):
            enterprise = factory.EnterpriseFactory.create()

            drivers = []
            for d_id in range(options["drivers"]):
                driver = factory.DriverFactory.create()
                driver.enterprise = enterprise
                driver.save()
                drivers.append(driver)

            for v_id in range(options["vehicles"]):
                # random Generate drivers list
                random_idx = random.randint(0, len(drivers)-1)
                random_idx_2 = random.randint(0, len(drivers)-1)
                left = min(random_idx, random_idx_2)
                right = max(random_idx, random_idx_2)
                vehicle = factory.VehicleFactory.create(drivers=drivers[left:right])
                vehicle.enterprise = enterprise
                saved_vehicles.append(vehicle)
                if len(saved_vehicles) % 10 == 0 and vehicle.drivers.all():
                    print('active_driver')
                    vehicle.active_driver = vehicle.drivers.all()[0]
                vehicle.save()

