from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets
# from api.websocket.consumers import GPSConsumer

router = DefaultRouter()

router.register(r"transaction", viewsets.TransactionViewset)
router.register(r"deployed_units", viewsets.DeployedUnitsViewSet)


urlpatterns = [
	path('', include(router.urls)),
	path('update_location/', viewsets.UpdateLocation.as_view()),
	# path('ws/gps/', GPSConsumer.as_asgi()),
]