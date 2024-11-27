from restaurants.models import Restaurant, RestaurantHour
from datetime import datetime, time
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


def parse_time(time_input):
    try:
        return datetime.strptime(time_input, "%I:%M %p").time()
    except ValueError:
        return datetime.strptime(time_input, "%I %p").time()


def parse_full_hours_line(full_line) -> list:
    combined = []
    for hours in full_line.split("/"):
        combined += parse_hours_input(hours)
    return combined


def parse_hours_input(hours_input) -> list:
    """
    split major sections on '/' BEFORE this
    get index of first numeral.
    get days section which may include multiple ranges split by comma
    covert char days to numeric 0-6

    """
    days_to_save = []
    hours_rows = []
    time_idx = get_num_index(hours_input)
    days_section = hours_input[:time_idx]
    for day_split in days_section.split(","):
        if "-" in day_split:
            days = day_split.split("-")
            day_start = DAYS.index(days[0].strip())
            day_end = DAYS.index(days[1].strip())
            days_to_save += list(range(day_start, day_end + 1))
        elif day_split:
            days_to_save.append(DAYS.index(day_split.strip()))

    start_time, end_time = [
        parse_time(t.strip()) for t in hours_input[time_idx:].split("-")
    ]
    if end_time < start_time:  # i.e. is open past midnight
        late_end_time = end_time
        late_days = [d + 1 if d < 6 else 0 for d in days_to_save]
        late_rows = [
            {"weekday": late_day, "opens_at": time(0), "closes_at": late_end_time}
            for late_day in late_days
        ]
        hours_rows += late_rows
        # mutate end_time
        end_time = parse_time("11:59 pm")

    hours_rows += [
        {"weekday": single_day, "opens_at": start_time, "closes_at": end_time}
        for single_day in days_to_save
    ]

    return hours_rows


def load_data_from_csv(file_path):
    with open(file_path, "r") as infile:
        reader = csv.DictReader(infile)
        loaded = 0
        for row in reader:
            restaurant_name = row["Restaurant Name"]
            if Restaurant.objects.filter(restaurant_name=restaurant_name).count():
                logging.info(f"{restaurant_name} already in database.\n")
                continue
            else:
                logging.info(f"Adding {restaurant_name}\n")
                restaurant = Restaurant(restaurant_name=restaurant_name)
                restaurant.save()

            for hours_data in parse_full_hours_line(row["Hours"]):
                hours_data["restaurant"] = restaurant
                hours_record = RestaurantHour(**hours_data)
                hours_record.save()
            loaded += 1

        logging.info(f"{loaded} rows loaded")
