from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/some_path/', consumers.WebSocketConsumer.as_asgi()),
    path('ws/dashboard/', consumers.DashboardMapConsumer.as_asgi()),
    path('ws/track_person/', consumers.TrackPersonConsumer.as_asgi()),
]