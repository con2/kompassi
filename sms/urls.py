from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import (
    sms_admin_votes_view,
    sms_admin_received_view,
)


urlpatterns = patterns(
    '',

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/sms/admin/?$',
        sms_admin_votes_view,
        name='sms_admin_votes_view',
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/sms/admin/received/?$',
        sms_admin_received_view,
        name='sms_admin_received_view',
    ),

)