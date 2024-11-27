from django.urls import path, include
from .views import RestaurantHourListApiView, RestaurantListFilterByOpen, readme_view


urlpatterns = [
    path("api/", RestaurantHourListApiView.as_view()),
    path("api/hours", RestaurantListFilterByOpen.as_view()),
    path("", readme_view, name="readme"),
]
