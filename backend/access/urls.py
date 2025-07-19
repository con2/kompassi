from django.urls import path, re_path

from .views.aliases_views import (
    access_admin_aliases_view,
    access_profile_aliases_view,
)
from .views.api_views import (
    access_admin_aliases_api,
    access_admin_group_emails_api,
    access_admin_group_members_api,
    api_discord_view,
)
from .views.privilege_views import (
    access_profile_privilege_view,
    access_profile_privileges_view,
    access_profile_request_privilege_view,
)
from .views.sudo_view import (
    sudo_view,
)

urlpatterns = [
    re_path(
        r"^profile/aliases/?$",
        access_profile_aliases_view,
        name="access_profile_aliases_view",
    ),
    re_path(
        r"^profile/privileges/?$",
        access_profile_privileges_view,
        name="access_profile_privileges_view",
    ),
    re_path(
        r"^profile/privileges/(?P<privilege_slug>[a-z0-9-]+)/?$",
        access_profile_privilege_view,
        name="access_profile_privilege_view",
    ),
    re_path(
        r"^profile/privileges/(?P<privilege_slug>[a-z0-9-]+)/request/?$",
        access_profile_request_privilege_view,
        name="access_profile_request_privilege_view",
    ),
    re_path(
        r"^api/v1/domains/(?P<domain_name>[a-z0-9-\.]+)/aliases.txt$",
        access_admin_aliases_api,
        name="access_admin_aliases_api",
    ),
    re_path(
        r"^api/v1/groups/(?P<group_name>[a-z0-9-]+)/emails.txt$",
        access_admin_group_emails_api,
        name="access_admin_group_emails_api",
    ),
    re_path(
        r"^api/v1/groups/(?P<group_name>[a-z0-9-]+)/members$",
        access_admin_group_members_api,
        name="access_admin_group_members_api",
    ),
    re_path(
        r"^api/v1/events/(?P<event_slug>[a-z0-9-]+)/discord/?$",
        api_discord_view,
        name="api_discord_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/admin/aliases/?$",
        access_admin_aliases_view,
        name="access_admin_aliases_view",
    ),
    path(
        "sudo",
        sudo_view,
        name="sudo_view",
    ),
]
