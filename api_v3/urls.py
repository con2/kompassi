from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views.api_v3_views import EventViewSet


class OptionalTrailingSlashRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.trailing_slash = '/?'


# Create a router and register our viewsets with it.
router = OptionalTrailingSlashRouter()
router.register(r'events', EventViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/v3/', include(router.urls)),
]
