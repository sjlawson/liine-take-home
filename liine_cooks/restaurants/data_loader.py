from restaurants.models import Restaurant, RestaurantHour
from datetime import datetime
import logging
import csv


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


def parse_time(time_input):
    try:
        return datetime.strptime(time_input, "%I:%M %p").time()
    except ValueError:
        return datetime.strptime(time_input, "%I %p").time()


def parse_full_hours_line(full_line):
    combined = []
    for hours in full_line.split('/'):
        combined.append(parse_hours_input(hours))
    return combined


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
    for day_split in days_section.split(','):
        if '-' in day_split:
            days = day_split.split('-')
            day_start = DAYS.index(days[0].strip())
            day_end = DAYS.index(days[1].strip())
            days_to_save += list(range(day_start, day_end+1))
        elif day_split:
            days_to_save.append(DAYS.index(day_split.strip()))

    start_time, end_time = [t.strip() for t in hours_input[time_idx:].split('-')]

    return {
        "days": days_to_save,
        "opens_at": parse_time(start_time),
        "closes_at": parse_time(end_time)}
