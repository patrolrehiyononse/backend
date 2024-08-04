from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


# router = DefaultRouter()

# router.register(r"dashboard", viewsets.DashboardTable)


urlpatterns = [
	path('dashboard/', viewsets.DashboardTable.as_view()),
	path('person_dropdown/', viewsets.PersonDropDown.as_view()),
	path('delete_all_path_traces/', viewsets.DeleteAllPathTraces.as_view()),
]