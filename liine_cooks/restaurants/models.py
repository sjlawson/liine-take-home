from django.db import models

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

    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    weekday = models.IntegerField(
        choices=Weekdays.choices,
        default=Weekdays.MON,
        verbose_name="Weekday",
    )
    opens_at = models.TimeField()
    closes_at = models.TimeField()

    def __str__(self):
        return f"{self.restaurant.restaurant_name}, {self.weekday}, {self.opens_at} - {self.closes_at}"
