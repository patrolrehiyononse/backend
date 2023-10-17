from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()

router.register(r"unit", viewsets.UnitViewset)
router.register(r"sub_unit", viewsets.SubUnitViewset)


urlpatterns = [
	path('', include(router.urls)),
	path('unit_choices/', viewsets.UnitDropDown.as_view(), name="unit_choices"),
	path('subunit_choices/', viewsets.SubUnitDropDown.as_view(), name="subunit_choices")
]