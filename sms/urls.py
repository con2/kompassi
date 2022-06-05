from django.conf.urls import include
from django.shortcuts import redirect

from .views import (
    sms_admin_votes_view,
    sms_admin_received_view,
)
from django.urls import re_path


urlpatterns = [
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/sms/admin/?$",
        sms_admin_votes_view,
        name="sms_admin_votes_view",
    ),
    re_path(
        r"^events/(?P<event_slug>[a-z0-9-]+)/sms/admin/received/?$",
        sms_admin_received_view,
        name="sms_admin_received_view",
    ),
]
