# encoding: utf-8

from __future__ import unicode_literals

from django.conf.urls import include, url

from .views import tracon2017_afterparty_participants_view


urlpatterns = [
    url(
        r'^events/(?P<event_slug>tracon2017)/survey/kaatoilmo/results.xlsx$',
        tracon2017_afterparty_participants_view,
        name='tracon2017_afterparty_participants_view',
    ),
]
