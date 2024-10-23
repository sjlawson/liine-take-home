from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RestaurantHour, Restaurant
from .serializers import RestaurantHourSerializer, RestaurantSerializer

import markdown


class RestaurantHourListApiView(APIView):

    def get(self, request, *args, **kwargs):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RestaurantListFilterByOpen(APIView):

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("datetime")
        restaurant_hours = RestaurantHour.get_open_restaurants_by_datetime(query)
        serializer = RestaurantHourSerializer(restaurant_hours, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def readme_view(request):
    readme_file = open("README.md", "r")
    readme = readme_file.read()
    md = markdown.Markdown(extensions=["fenced_code"])
    markdown_content = md.convert(readme)
    context = {"markdown_content": markdown_content}

    return render(request, "md_content.html", context=context)
