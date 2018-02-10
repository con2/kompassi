from django.conf.urls import include, url
from django.conf import settings

from csp.decorators import csp_exempt
from oauth2_provider.views.base import AuthorizationView, TokenView, RevokeTokenView

from .views import MyselfResource, EventResource


assert 'oauth2_provider' in settings.INSTALLED_APPS, 'api_v2 requires oauth2_provider'


urlpatterns = [
    url(
        r'^oauth2/authorize/?$',
        csp_exempt(AuthorizationView.as_view()),
        name="authorize"
    ),

    url(
        r'^oauth2/token/?$',
        csp_exempt(TokenView.as_view()),
        name="token"
    ),

    url(
        r'^oauth2/revoke/?$',
        csp_exempt(RevokeTokenView.as_view()),
        name="revoke"
    ),

    url(
        r'^api/v2/people/me?$',
        csp_exempt(MyselfResource.as_view()),
        name='api_v2_self_resource'
    ),

    url(
        r'^api/v2/events/(?P<event_slug>[a-z0-9-]+)/?$',
        csp_exempt(EventResource.as_view()),
        name='api_v2_event_resource'
    ),

]
