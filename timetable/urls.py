from django.conf.urls import patterns, include, url

from .views import timetable_view

urlpatterns = patterns('',
    url(r'^$', timetable_view, name='timetable_view')
)
