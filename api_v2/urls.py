from django.conf.urls import patterns, include, url
from django.conf import settings

from oauth2_provider.views.base import AuthorizationView, TokenView

from .views import MyselfResource

assert 'oauth2_provider' in settings.INSTALLED_APPS, 'api_v2 requires oauth2_provider'

urlpatterns = patterns('',
    url(r'^oauth2/authorize/?$', AuthorizationView.as_view(), name="authorize"),
    url(r'^oauth2/token/?$', TokenView.as_view(), name="token"),
    url(r'^api/v2/people/me?$', MyselfResource.as_view(), name='api_v2_self_resource'),
)
