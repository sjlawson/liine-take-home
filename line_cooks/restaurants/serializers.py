from rest_framework import serializers
from .models import RestaurantHour, Restaurant


class RestaurantHourSerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField(many=False, read_only=True)
    weekday = serializers.SerializerMethodField()
    opens_at = serializers.SerializerMethodField()
    closes_at = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantHour
        # if we only want a list of restaurant names, eliminate the other fields here
        # however, in a real-worl scenario I think these would be included
        fields = ["restaurant", "weekday", "opens_at", "closes_at"]

    def get_weekday(self, obj):
        return obj.get_weekday_display()

    def get_opens_at(self, obj):
        return obj.get_open_time()

    def get_closes_at(self, obj):
        return obj.get_close_time()


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "restaurant_name",
        ]
