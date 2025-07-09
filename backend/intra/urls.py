from django.urls import re_path

from .views import (
    intra_admin_privileges_view,
    intra_admin_team_member_view,
    intra_organizer_view,
)
from .views.intra_api_teams_view import intra_api_teams_view, intra_teams_fragment_view

app_name = "intra"
urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/?$",
        intra_organizer_view,
        name="organizer_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/people\.(?P<format>\w+)$",
        intra_organizer_view,
        name="organizer_export_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/admin/teams/(?P<team_slug>[a-z0-9-]+)/members/new/?$",
        intra_admin_team_member_view,
        name="admin_team_add_member_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/admin/privileges/?$",
        intra_admin_privileges_view,
        name="admin_privileges_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/admin/people/(?P<person_id>\d+)/teams/new/?$",
        intra_admin_team_member_view,
        name="admin_member_add_team_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/intra/admin/teams/(?P<team_slug>[a-z0-9-]+)/members/(?P<person_id>\d+)/?$",
        intra_admin_team_member_view,
        name="admin_team_member_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/teams/?$",
        intra_api_teams_view,
        name="api_teams_view",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/teams.html$",
        intra_teams_fragment_view,
        name="teams_fragment_view",
    ),
]
