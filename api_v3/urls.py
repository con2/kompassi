from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.views.api_v3_views import EventViewSet

from .views import CurrentUserView


class OptionalTrailingSlashRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.trailing_slash = '/?'


# Create a router and register our viewsets with it.
router = OptionalTrailingSlashRouter()
router.register(r'events', EventViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    re_path(r'^api/v3/user/?$', CurrentUserView.as_view(), name='api_v3_current_user_view'),
    path('api/v3/', include(router.urls)),
]
