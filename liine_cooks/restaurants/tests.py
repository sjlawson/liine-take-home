from django.test import TestCase
from restaurants.models import Restaurant, RestaurantHour
from restaurants.data_loader import parse_hours_input, parse_full_hours_line
from datetime import time


VALID_OPEN = "2024-10-23T21:22"
CLOSED_HOURS = "2024-10-23T21:45"


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

    def test_restaurant_not_open(self):
        closed_hours_test = RestaurantHour.get_open_restaurants_by_datetime(
            CLOSED_HOURS).first()
        self.assertIsNone(closed_hours_test)


class LoaderTestCase(TestCase):

    def test_simple_hour_string_parses(self):
        simple_hours = "Mon-Sat 11 am - 9:30 pm"
        parsed = parse_hours_input(simple_hours)

        self.assertEqual(parsed['days'], [0, 1, 2, 3, 4, 5,])
        self.assertEqual(parsed['opens_at'], time(11))
        self.assertEqual(parsed['closes_at'], time(21, 30))

    def test_complex_hour_parses(self):
        complex_hours = "Tues-Thu, Sat 10:30 am - 9 pm"
        parsed = parse_hours_input(complex_hours)
        self.assertEqual(parsed['days'], [1, 2, 3, 5])
        self.assertEqual(parsed['opens_at'], time(10, 30))
        self.assertEqual(parsed['closes_at'], time(21))

    def test_full_line_hour_parses(self):
        full_hours_line = "Tues-Thu, Sat 10:30 am - 9 pm / Sun 11 am - 8 pm"
        parsed = parse_full_hours_line(full_hours_line)
        breakpoint()
        self.assertEqual(parsed['days'], [1, 2, 3, 5])
        self.assertEqual(parsed['opens_at'], time(10, 30))
        self.assertEqual(parsed['closes_at'], time(21))
