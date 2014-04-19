from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import programme_timetable_view


urlpatterns = patterns('',
    url(r'^$', programme_timetable_view, dict(event_slug='tracon8'), name='core_frontpage_view'),
    url(r'', include('turska.urls')), 
)
