from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"station", viewsets.StationViewset)
# router.register(r"sub_station", viewsets.SubStationViewset)


urlpatterns = [
	path('', include(router.urls)),
	# path('/transaction_search', viewsets.TransactionSearchViewset.as_view(), name="search")
]