from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import RestaurantHour
from .serializers import RestaurantHourSerializer


class RestaurantHourListApiView(APIView):

    def get(self, request, *args, **kwargs):
        request_datetime = request.query_params['datetime'])
        # str: 2024-10-18T17:30
        restaurant_hours = RestaurantHour.objects.all()
        serializer = RestaurantHourSerializer(restaurant_hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
