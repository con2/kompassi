from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import (
    access_profile_aliases_view,
    access_profile_privileges_view,
    access_profile_request_privilege_view,
    access_admin_aliases_api,
)

urlpatterns = patterns('',
    url(
        r'^profile/aliases/?$',
        access_profile_aliases_view,
        name='access_profile_aliases_view',
    ),

    url(
        r'^profile/privileges/?$',
        access_profile_privileges_view,
        name='access_profile_privileges_view',
    ),

    url(
        r'^profile/privileges/(?P<privilege_slug>[a-z0-9-]+)/request/?$',
        access_profile_request_privilege_view,
        name='access_profile_request_privilege_view',
    ),

    url(
        r'^api/v1/domains/(?P<domain_name>[a-z0-9-\.]+)/aliases.txt$',
        access_admin_aliases_api,
        name='access_admin_aliases_api',
    )
)
