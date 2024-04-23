from django.core.management.base import BaseCommand
import random

from . import _factories as factory


class Command(BaseCommand):
    help = "Generate enterprise data"
    _MAX_DRIVERS_FOR_VEHICLE = 10

    def add_arguments(self, parser):
        parser.add_argument("--enterprise", type=int, default=1)
        parser.add_argument("--vehicles", type=int, default=3)
        parser.add_argument("--drivers", type=int, default=5)

    def log(self, string):
        self.stdout.write(
            self.style.SUCCESS(string)
        )

    def handle(self, *args, **options):
        saved_vehicles = []
        for e_id in range(options["enterprise"]):
            enterprise = factory.EnterpriseFactory.create()
            enterprise.save()
            # self.log(f'create enterprise: {enterprise}')

            drivers = set()
            for d_id in range(options["drivers"]):
                driver = factory.DriverFactory.create()
                driver.enterprise = enterprise
                driver.save()
                drivers.add(driver)
                # self.log(f'create driver: {driver}')

            active_drivers = set()
            max_drivers_count = min(self._MAX_DRIVERS_FOR_VEHICLE, options["drivers"])
            for v_id in range(options["vehicles"]):
                # random Generate drivers list
                min_drivers_count = random.randint(3, max_drivers_count)
                curent_drivers = []
                for _ in range(min_drivers_count, max_drivers_count):
                    curent_drivers.append(list(drivers)[random.randint(0, len(drivers) - 1)])
                vehicle = factory.VehicleFactory.create(drivers=curent_drivers)
                vehicle.enterprise = enterprise
                saved_vehicles.append(vehicle)
                free_drivers = set(vehicle.drivers.all()) - active_drivers
                if len(saved_vehicles) % 10 == 0 and free_drivers:
                    active_driver = list(free_drivers)[0]
                    vehicle.active_driver = active_driver
                    self.log(f'set active_driver for vehicle: {vehicle}')
                    active_drivers.add(active_driver)
                vehicle.save()
                # self.log(f'create vehicle: {vehicle}')
            self.log(f'Total active_drivers: {len(active_drivers)}')
        self.log('Process complete successfull...')

