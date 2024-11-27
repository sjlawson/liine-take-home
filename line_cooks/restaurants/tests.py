from django.test import TestCase
from restaurants.models import Restaurant, RestaurantHour
from restaurants.data_loader import parse_hours_input, parse_full_hours_line
from datetime import time


VALID_OPEN = "2024-10-23T21:22"  # wed / 2
CLOSED_HOURS = "2024-10-23T21:45"

AFTER_MIDNIGHT_VALID_OPEN = "2024-10-24T17:20"  # thurs / 3
AFTER_MIDNIGHT_CLOSED = "2024-10-25T03:20"  # fri / 4


class RestaurantTestCase(TestCase):
    def setUp(self):
        restaurant = Restaurant(restaurant_name="Local Pub")
        restaurant.save()
        restaurant_hour = RestaurantHour(
            restaurant=restaurant, weekday=2, opens_at=time(11), closes_at=time(21, 30)
        )
        restaurant_hour.save()

        # need to test for restaurants with hours that go past midnight
        late_restaurant = Restaurant(restaurant_name="Late Nights!!")
        late_restaurant.save()
        late_restaurant_hour = RestaurantHour(
            restaurant=late_restaurant,
            weekday=3,
            opens_at=time(17),
            closes_at=time(23, 59),
        )
        late_restaurant_hour.save()
        extra_late = RestaurantHour(
            restaurant=late_restaurant,
            weekday=4,
            opens_at=time(0),
            closes_at=time(2, 30),
        )
        extra_late.save()

    def test_restaurant_hours_filter_during_open_hours(self):
        open_hours_test = RestaurantHour.get_open_restaurants_by_datetime(
            VALID_OPEN
        ).first()
        self.assertEqual(open_hours_test.restaurant.restaurant_name, "Local Pub")

    def test_restaurant_not_open(self):
        closed_hours_test = RestaurantHour.get_open_restaurants_by_datetime(
            CLOSED_HOURS
        ).first()
        self.assertIsNone(closed_hours_test)

    def test_late_night_open(self):
        open_late = RestaurantHour.get_open_restaurants_by_datetime(
            AFTER_MIDNIGHT_VALID_OPEN
        ).first()
        self.assertEqual(open_late.restaurant.restaurant_name, "Late Nights!!")

    def test_late_night_closed(self):
        late_still_closed = RestaurantHour.get_open_restaurants_by_datetime(
            AFTER_MIDNIGHT_CLOSED
        ).first()
        self.assertIsNone(late_still_closed)


class LoaderTestCase(TestCase):

    def test_simple_hour_string_parses(self):
        simple_hours = "Mon-Sat 11 am - 9:30 pm"
        parsed = parse_hours_input(simple_hours)

        self.assertEqual(parsed[2]["weekday"], 2)
        self.assertEqual(parsed[3]["opens_at"], time(11))
        self.assertEqual(parsed[5]["closes_at"], time(21, 30))

        parsed_list = parse_full_hours_line(simple_hours)
        self.assertListEqual(
            parsed, parsed_list
        )  # for simple hours these should be the same

    def test_complex_hour_parses(self):
        complex_days = "Tues-Thu, Sat 10:30 am - 9 pm"
        parsed = parse_hours_input(complex_days)
        self.assertEqual([p["weekday"] for p in parsed], [1, 2, 3, 5])
        self.assertEqual(parsed[2]["opens_at"], time(10, 30))
        self.assertEqual(parsed[3]["closes_at"], time(21))

    def test_full_line_hour_parses(self):
        full_hours_line = "Tues-Thu, Sat 10:30 am - 9 pm / Sun 11 am - 8 pm"
        parsed = parse_full_hours_line(full_hours_line)

        self.assertEqual([p["weekday"] for p in parsed], [1, 2, 3, 5, 6])
        self.assertEqual(parsed[0]["opens_at"], time(10, 30))
        self.assertEqual(parsed[0]["closes_at"], time(21))

        self.assertEqual(parsed[4]["weekday"], 6)
        self.assertEqual(parsed[4]["opens_at"], time(11))
        self.assertEqual(parsed[4]["closes_at"], time(20))

        multi_line_hours = (
            "Mon-Wed 5 pm - 12:30 am  / Thu-Fri 5 pm - 1:30 am  /"
            " Sat 3 pm - 1:30 am  / Sun 3 pm - 11:30 pm"
        )

        parsed = parse_full_hours_line(multi_line_hours)
        self.assertListEqual(
            parsed,
            [
                {"weekday": 1, "opens_at": time(0, 0), "closes_at": time(0, 30)},
                {"weekday": 2, "opens_at": time(0, 0), "closes_at": time(0, 30)},
                {"weekday": 3, "opens_at": time(0, 0), "closes_at": time(0, 30)},
                {"weekday": 0, "opens_at": time(17, 0), "closes_at": time(23, 59)},
                {"weekday": 1, "opens_at": time(17, 0), "closes_at": time(23, 59)},
                {"weekday": 2, "opens_at": time(17, 0), "closes_at": time(23, 59)},
                {"weekday": 4, "opens_at": time(0, 0), "closes_at": time(1, 30)},
                {"weekday": 5, "opens_at": time(0, 0), "closes_at": time(1, 30)},
                {"weekday": 3, "opens_at": time(17, 0), "closes_at": time(23, 59)},
                {"weekday": 4, "opens_at": time(17, 0), "closes_at": time(23, 59)},
                {"weekday": 6, "opens_at": time(0, 0), "closes_at": time(1, 30)},
                {"weekday": 5, "opens_at": time(15, 0), "closes_at": time(23, 59)},
                {"weekday": 6, "opens_at": time(15, 0), "closes_at": time(23, 30)},
            ],
        )
