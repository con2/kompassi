# encoding: utf-8

from __future__ import unicode_literals

from django.conf.urls import include, url

from .views import tracon11_afterparty_participants_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>tracon11)/survey/kaatoilmo/results.xlsx$',
        tracon11_afterparty_participants_view,
        name='tracon11_afterparty_participants_view',
    ),
]
