
from django.urls import path, include
from .views import RestaurantHourListApiView


urlpatterns = [
    path('api/', RestaurantHourListApiView.as_view()),
]
