from csp.decorators import csp_exempt
from django.conf import settings
from django.conf.urls import include
from django.urls import path, re_path
from oauth2_provider.views.base import RevokeTokenView, TokenView

from .views import CustomAuthorizationView, EventResource, MyselfResource

assert "oauth2_provider" in settings.INSTALLED_APPS, "api_v2 requires oauth2_provider"


urlpatterns = [
    # overridden to implement email verification check
    re_path(
        r"^oidc/authorize/$",
        csp_exempt(CustomAuthorizationView.as_view()),
        name="authorize-kompassi-override",
    ),
    re_path(r"^oauth2/authorize/?$", csp_exempt(CustomAuthorizationView.as_view()), name="authorize"),
    # standards-compliant oidc provider
    path("oidc/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    # legacy oauth2 endpoints
    re_path(r"^oauth2/token/?$", csp_exempt(TokenView.as_view()), name="token"),
    re_path(r"^oauth2/revoke/?$", csp_exempt(RevokeTokenView.as_view()), name="revoke"),
    re_path(r"^api/v2/people/me?$", csp_exempt(MyselfResource.as_view()), name="api_v2_self_resource"),
    re_path(
        r"^api/v2/events/(?P<event_slug>[a-z0-9-]+)/?$",
        csp_exempt(EventResource.as_view()),
        name="api_v2_event_resource",
    ),
]
