from django.test import TestCase
from restaurants.models import Restaurant, RestaurantHour
from restaurants.data_loader import parse_hours_input
from datetime import time


VALID_OPEN = "2024-10-23T21:22"
CLOSED_HOURS = "2024-10-23T21:45"


# Create your tests here.
class RestaurantTestCase(TestCase):
    def setUp(self):
        restaurant = Restaurant(restaurant_name="Local Pub")
        restaurant.save()
        restaurant_hour = RestaurantHour(
            restaurant=restaurant,
            weekday=2,
            opens_at=time(11),
            closes_at=time(21, 30)
        )
        restaurant_hour.save()

    def test_restaurant_hours_filter_during_open_hours(self):
        open_hours_test = RestaurantHour.get_open_restaurants_by_datetime(
            VALID_OPEN).first()
        self.assertEqual(open_hours_test.restaurant.restaurant_name, "Local Pub")


class LoaderTestCase(TestCase):

    def test_simple_hour_string_parses(self):
        simple_hours = "Mon-Sun 11 am - 12 am"
        parsed = parse_hours_input(simple_hours)
        self.assertEqual(parsed['days'], [0, 1, 2, 3, 4, 5, 6,])
        self.assertEqual(parsed['opens_at'], time(11))
        self.assertEqual(parsed['closes_at'], time(21, 30))
