from rest_framework import serializers
from .models import RestaurantHour


class RestaurantHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantHour
        fields = ["restaurant", "weekday", "opens_at", "closes_at"]
