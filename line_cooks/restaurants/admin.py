from django.contrib import admin
from .models import Restaurant, RestaurantHour


@admin.register(Restaurant, RestaurantHour)
class RestaurantAdmin(admin.ModelAdmin):
    pass
