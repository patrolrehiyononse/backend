from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


# router = DefaultRouter()

# router.register(r"dashboard", viewsets.DashboardTable)


urlpatterns = [
	path('login/', viewsets.CustomLogin.as_view(), name='login'),
	path('request_code/', viewsets.RequestCode.as_view(), name="request_code"),
	path('verify_code/', viewsets.VerifyCode.as_view(), name="verify_code")
]