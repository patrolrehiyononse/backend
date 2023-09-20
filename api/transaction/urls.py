from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"transaction", viewsets.TransactionViewset)


urlpatterns = [
	path('', include(router.urls)),
	path('update_location/', viewsets.UpdateLocation.as_view())
]