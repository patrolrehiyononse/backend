from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"rank", viewsets.RankViewset)


urlpatterns = [
	path('', include(router.urls)),
	path('rank_choices/', viewsets.RankDropDown.as_view(), name="rank_choices")
]