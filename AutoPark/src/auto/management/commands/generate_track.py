from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
import random
import openrouteservice
from datetime import datetime, timedelta, timezone
from geopy.distance import distance

from auto.models import Geotag, Vehicle, Trip
from app.settings import env


class Command(BaseCommand):
    help = "Generate track data for car"

    # формат - долгота, широта.
    _STARTS = (
        (37.49633789062501, 56.09167209613758),  # МСК
        (31.208446025848392, 58.50529239107178),  # Новгород
        (30.312438011169437, 59.96545122540727),  # СПБ
    )
    _ENDS = (
        (30.503711700439457, 59.83187739239028),
        (37.50303268432618, 55.25706096501312),
        (30.501512289047245, 59.831855825748406),  # МСК

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
        start = self._STARTS[random.randint(0, len(self._STARTS) - 1)]
        end = self._ENDS[random.randint(0, len(self._ENDS) - 1)]
        round = options.get("round")
        routes = client.directions(
            [start, end] if not round else start,
            format='geojson',
            options={} if not round else req_options,
            validate=False,
        )
        points = self.points(routes)
        prev_point = points[0]
        step = options.get("step")
        last_trip = Trip.objects.order_by("-end_date").first()
        now = datetime.now() if not last_trip else last_trip.end_date
        now = datetime(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second,
            tzinfo=timezone.utc
        )
        now += timedelta(minutes=5)
        # some hack for zero init
        distance_sum = distance(prev_point, prev_point)
        vehicle = Vehicle.objects.get(id=options.get("vehicle_id"))
        for point in points[1::step]:
            distance_sum += distance(prev_point, point)
            prev_point = point
            orm_point = Geotag(
                point=Point(point[1], point[0]),  # у сервиса визуализации яндекса формат широта/долгота
                vehicle=vehicle,
                timestamp=now
            )
            print(*point[::-1])
            print(now)
            orm_point.save()
            if distance_sum.km >= limit:
                self.log("limit by km")
                break
            self.log(f"distance is: {distance_sum.km} km")
            now += timedelta(seconds=10)

    @staticmethod
    def points(routes):
        return routes["features"][0]["geometry"]["coordinates"]