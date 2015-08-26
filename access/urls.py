from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from .views import (
    access_profile_privileges_view,
    access_profile_request_privilege_view,
)

urlpatterns = patterns('',
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
)
