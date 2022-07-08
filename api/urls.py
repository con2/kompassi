from django.conf.urls import include

from .views import api_discord_view, api_person_view, api_status_view
from django.urls import re_path


urlpatterns = [
    re_path(r"^api/v1/people/(?P<username>[a-zA-Z0-9_]+)/?$", api_person_view, name="api_person_view"),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/discord/?$",
        api_discord_view,
        name="api_discord_view",
    ),
    re_path(r"^api/v1/status/?$", api_status_view, name="api_status_view"),
]
