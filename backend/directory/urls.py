from django.urls import re_path

from .views import directory_person_view, directory_view

app_name = "directory"

urlpatterns = [
    re_path(r"^organizations/(?P<organization_slug>[a-z0-9-]+)/people/?$", directory_view, name="directory_view"),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/people/(?P<person_id>[0-9]+)/?$",
        directory_person_view,
        name="directory_person_view",
    ),
]
