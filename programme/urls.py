from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import *

urlpatterns = patterns('',
    url(r'^events/(?P<event_id>[a-z0-9-]+)/timetable/?$', timetable_view, name='programme_timetable_view'),
    url(r'^events/(?P<event_id>[a-z0-9-]+)/timetable/mobile/?$', mobile_timetable_view, name='programme_mobile_timetable_view'),
    url(r'^events/(?P<event_id>[a-z0-9-]+)/timetable/mobile/(\d{1,4})', mobile_programme_detail_view, name='mobile_programme_detail_view'),
    url(r'^events/(?P<event_id>[a-z0-9-]+)/timetable/full$', internal_timetable_view, name='programme_internal_timetable_view'),
    url(r'^events/(?P<event_id>[a-z0-9-]+)/timetable.taggedtext$', internal_adobe_taggedtext_view, name='programme_internal_adobe_taggedtext_view')
)
