from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.i18n import set_language

handler404 = "access.views.not_found_view"
handler403 = "access.views.permission_denied_view"

kompassi_apps = [
    "labour",
    "programme",
    "tickets",
    "tickets_v2",
    "payments",
    "api",
    "api_v2",
    "graphql_api",
    "badges",
    "access",
    "desuprofile_integration",
    "membership",
    "enrollment",
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

urlpatterns = [
    path("", include("core.urls")),
    path("admin", RedirectView.as_view(url="/admin/", permanent=False)),
    path("admin/", admin.site.urls),
    re_path(r"^i18n/setlang/?$", set_language, name="set_language"),
    *(path("", include(f"{app_name}.urls")) for app_name in kompassi_apps if app_name in settings.INSTALLED_APPS),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
