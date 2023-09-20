from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"person", viewsets.PersonViewset)


urlpatterns = [
	path('', include(router.urls))
]