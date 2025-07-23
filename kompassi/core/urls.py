from django.urls import path, re_path

from .views import (
    core_admin_impersonate_view,
    core_email_verification_request_view,
    core_email_verification_view,
    core_event_view,
    core_fobba_export_view,
    core_frontpage_view,
    core_login_view,
    core_logout_view,
    core_organization_view,
    core_organizations_view,
    core_password_reset_request_view,
    core_password_reset_view,
    core_password_view,
    core_personify_view,
    core_profile_view,
    core_registration_view,
    core_stats_view,
)

urlpatterns = [
    path("", core_frontpage_view, name="core_frontpage_view"),
    re_path(
        r"^events/?$",
        core_frontpage_view,
        dict(template="core_events_view.pug", include_past_events=True),
        name="core_events_view",
    ),
    re_path(r"^events/(?P<event_slug>[a-z0-9-]+)/?$", core_event_view, name="core_event_view"),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/fobba.xlsx$",
        core_fobba_export_view,
        name="core_fobba_export_view",
    ),
    re_path(
        r"^organizations/?$",
        core_organizations_view,
        name="core_organizations_view",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[a-z0-9-]+)/?$",
        core_organization_view,
        name="core_organization_view",
    ),
    path("login", core_login_view, name="core_login_view"),
    path("logout", core_logout_view, name="core_logout_view"),
    path("register", core_registration_view, name="core_registration_view"),
    path("profile", core_profile_view, name="core_profile_view"),
    path("profile/new", core_personify_view, name="core_personify_view"),
    path("profile/password", core_password_view, name="core_password_view"),
    path("profile/password/reset", core_password_reset_request_view, name="core_password_reset_request_view"),
    re_path(
        r"^profile/password/reset/(?P<code>[a-f0-9]+)$",
        core_password_reset_view,
        name="core_password_reset_view",
    ),
    path(
        "profile/email/verify",
        core_email_verification_request_view,
        name="core_email_verification_request_view",
    ),
    re_path(
        r"^profile/email/verify/(?P<code>[a-f0-9]+)$",
        core_email_verification_view,
        name="core_email_verification_view",
    ),
    re_path(
        r"^impersonate/(?P<username>[a-zA-Z0-9_-]+)$",
        core_admin_impersonate_view,
        name="core_admin_impersonate_view",
    ),
    path("stats", core_stats_view, name="core_stats_view"),
]
