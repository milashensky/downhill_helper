from django.urls import path
from sensors.api import SensorSignalApi


urlpatterns = [
    path('signal', SensorSignalApi.as_view(), name='signal_api'),
]
