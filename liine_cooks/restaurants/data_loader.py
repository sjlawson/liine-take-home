from restaurants.models import Restaurant, RestaurantHour
from datetime import time
import logging
import csv
import re


DAYS = [
    "Mon",
    "Tues",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]


def get_num_index(h_in: str) -> int:
        for cha in h_in:
            if cha.isdigit():
                return h_in.index(cha)


def load_data_from_csv():
    with open("../../restaurants.csv", "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            restaurant_name = row['Restaurant Name']
            check_name = Restaurant.objects.filter(restaurant_name=restaurant_name)
            if check_name.count():
                logging.info(f"{restaurant_name} already in database.\n")
                continue
            restaurant = Restaurant(restaurant_name=restaurant_name)
            restaurant.save()


def parse_hours_input(hours_input):
    """
    split major sections on '/' BEFORE this
    get index of first numeral.
    get days section which may include multiple ranges split by comma
    covert char days to numeric 0-6

    """
    days_to_save = []

    time_idx = get_num_index(hours_input)
    days_section = hours_input[:time_idx]
    pattern = "(?P<range>[a-zA-Z]{3,4}-[a-zA-Z]{3,4})[, ]*(?P<single>[a-zA-Z]{3,4})"
    matches = re.search(pattern, days_section)
    match_groups = matches.groupdisct()

    if day_range := match_groups['range']:
        days = "-".split(day_range)
        day_start = DAYS.index(days[0])
        day_end = DAYS.index(days[1])
        days_to_save += list(range(day_start, day_end+1))

    if single_day := match_groups['single']:
        days_to_save.append(DAYS.index(single_day))

    start_time, end_time = [t.strip() for t in '-'.split(hours_input[time_idx:])]

    return {"days": days_to_save, "opens_at": time(0), "closes_at": time(0)}
