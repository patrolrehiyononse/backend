from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"station", viewsets.StationViewset)


urlpatterns = [
	path('', include(router.urls)),
	path('station_choices/', viewsets.StationDropDown.as_view(), name="station_choices")
]