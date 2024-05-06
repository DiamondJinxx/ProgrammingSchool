from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
import random
import openrouteservice
from datetime import datetime, timedelta
from geopy.distance import distance

from auto.models import Geotag, Vehicle
from app.settings import env


class Command(BaseCommand):
    help = "Generate track data for car"

    _COORDINATES = (
        (
            # Воронеж. Улица Улица Чапаева - Связной
            (51.66797728159497, 39.19218063354493),
            (51.64614620689681, 39.18445587158204)
        ),
        (
            # Москва, Противоположные точки на МКАДе
            (55.58688295920994, 37.51831054687501),
            (55.58998733044274, 37.73391723632813)
        ),
    )

    def add_arguments(self, parser):
        parser.add_argument("--vehicle_id", type=int)
        parser.add_argument("--limit", type=int, default=3)
        parser.add_argument("--step", type=int, default=1)
        parser.add_argument("--round", type=bool, default=False)

    def log(self, msg):
        self.stdout.write(
            self.style.SUCCESS(msg)
        )

    def error(self, msg):
        self.stdout.write(
            self.style.ERROR(msg)
        )

    def handle(self, *args, **options):
        if options.get("vehicle_id") is None:
            self.error("vehicle_id must be defined")
        api_key = env("ROUTS_API_KEY")
        limit = options.get("limit")
        req_options = {
            "round_trip": {
                "length": limit * 1000,
                "points": 3,
                "seed": 0
            }
        }
        client = openrouteservice.Client(key=api_key)
        coord = self._COORDINATES[random.randint(0, len(self._COORDINATES) - 1)]
        round = options.get("round")
        routes = client.directions(
            coord if not round else coord[0],
            format='geojson',
            options={} if not round else req_options,
            validate=False,
        )
        points = self.points(routes)
        prev_point = points[0]
        step = options.get("step")
        now = datetime.now()
        # some hack for zero init
        distance_sum = distance(prev_point, prev_point)
        vehicle = Vehicle.objects.get(id=options.get("vehicle_id"))
        for point in points[1::step]:
            distance_sum += distance(prev_point, point)
            prev_point = point
            orm_point = Geotag(
                point=Point(*point),
                vehicle=vehicle,
                timestamp=now
            )
            print(now)
            orm_point.save()
            if distance_sum.km >= limit:
                self.log("limit by km")
                break
            now += timedelta(seconds=10)

    @staticmethod
    def points(routes):
        return routes["features"][0]["geometry"]["coordinates"]