from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.i18n import set_language

handler404 = "kompassi.access.views.error_views.not_found_view"
handler403 = "kompassi.access.views.error_views.permission_denied_view"

kompassi_apps = [
    "labour",
    "tickets_v2",
    "payments",
    "api",
    "api_v2",
    "graphql_api",
    "badges",
    "access",
    "desuprofile_integration",
    "membership",
    "intra",
    "feedback",
    "directory",
    "listings",
    "metrics",
    "forms",
    "emprinten",
    "program_v2",
    "events.frostbite2025",
]

zombie_apps = [
    "programme",
    "tickets",
    "enrollment",
]

urlpatterns = [
    path("", include("kompassi.core.urls")),
    path("admin", RedirectView.as_view(url="/admin/", permanent=False)),
    path("admin/", admin.site.urls),
    re_path(r"^i18n/setlang/?$", set_language, name="set_language"),
    *(path("", include(f"kompassi.{app_name}.urls")) for app_name in kompassi_apps),
    *(path("", include(f"kompassi.zombies.{app_name}.urls")) for app_name in zombie_apps),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
