from django.db import models
from datetime import datetime


# Create your models here.
class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200)

    def __str__(self):
        return self.restaurant_name


class RestaurantHour(models.Model):
    class Weekdays(models.IntegerChoices):
        MON = 0, "Mon"
        TUE = 1, "Tues"
        WED = 2, "Wed"
        THU = 3, "Thu"
        FRI = 4, "Fri"
        SAT = 5, "Sat"
        SUN = 6, "Sun"

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="hours"
    )
    weekday = models.IntegerField(
        choices=Weekdays.choices,
        default=Weekdays.MON,
        verbose_name="Weekday",
    )
    opens_at = models.TimeField()
    closes_at = models.TimeField()

    def __str__(self):
        return f"{self.restaurant.restaurant_name}, {self.weekday}, {self.opens_at} - {self.closes_at}"

    def get_open_time(self):
        return self.opens_at.strftime("%I:%M %p")

    def get_close_time(self):
        return self.closes_at.strftime("%I:%M %p")

    @staticmethod
    def get_open_restaurants_by_datetime(query):
        if not query:
            return None

        request_datetime = datetime.strptime(query, "%Y-%m-%dT%H:%M")
        req_time = request_datetime.time()
        req_weekday = request_datetime.weekday()

        restaurant_hours = RestaurantHour.objects.filter(
            weekday=req_weekday,
            opens_at__lte=req_time,
            closes_at__gte=req_time
        )

        return restaurant_hours
