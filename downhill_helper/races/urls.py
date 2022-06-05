from django.urls import path
from races.api import RaceApi, QualificationApi, BracketsApi

urlpatterns = [
    path('api/race/<str:race_slug>', RaceApi.as_view(), name='race_api'),
    path('api/race/<str:race_slug>/qualification', QualificationApi.as_view(), name='qualification_api'),
    path('api/race/<str:race_slug>/brackets/<int:type>/', BracketsApi.as_view(), name='brackets_api'),
]
