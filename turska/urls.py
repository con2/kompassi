# encoding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt

from graphene.contrib.django.views import GraphQLView

from .schema import schema


urlpatterns = [
    url(r'', include('core.urls')),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
    url(r'^graphiql', include('django_graphiql.urls')),
]

for app_name in [
    'labour',
    'programme',
    'tickets',
    'payments',
    'api',
    'api_v2',
    'badges',
    'access',
    'nexmo',
    'sms',
    'desuprofile_integration',
    'membership',
]:
    if app_name in settings.INSTALLED_APPS:
        urlpatterns.append(url(r'', include('{app_name}.urls'.format(app_name=app_name))))
