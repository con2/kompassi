from django.urls import re_path

from .views import api_person_view, api_status_view

urlpatterns = [
    re_path(
        r"^api/v1/people/(?P<username>[a-zA-Z0-9_]+)/?$",
        api_person_view,  # type: ignore
        name="api_person_view",
    ),
    re_path(
        r"^api/v1/status/?$",
        api_status_view,  # type: ignore
        name="api_status_view",
    ),
]
