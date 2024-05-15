from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"geofencing", viewsets.GeofencingViewset)


urlpatterns = [
	path('', include(router.urls)),
	path('get_geofencing/', viewsets.GetGeofencing.as_view())
]