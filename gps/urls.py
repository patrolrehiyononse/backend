from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.websocket import routing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.transaction.urls")),
    path('api/', include("api.rank.urls")),
    path('api/', include("api.unit.urls")),
    path('api/', include("api.person.urls")),
    path('api/', include("api.dashboard.urls")),
    path('api/', include("api.station.urls")),
    path('api/', include("api.login.urls")),
    path('', include(routing.websocket_urlpatterns)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
