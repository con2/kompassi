from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import (
    sms_admin_dashboard_view,
)


urlpatterns = patterns(
    '',

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/sms/admin/?$',
        sms_admin_dashboard_view,
        name='sms_admin_dashboard_view',
    ),

)