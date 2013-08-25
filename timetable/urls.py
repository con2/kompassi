from django.conf.urls import patterns, include, url

from .views import timetable_view, internal_dumpdata_view, internal_timetable_view, internal_adobe_taggedtext_view

urlpatterns = patterns('',
    url(r'^$', timetable_view, name='timetable_view'),
    url(r'^extranet/timetable$', internal_timetable_view, name='internal_timetable_view'),
    url(r'^data\.json$', internal_dumpdata_view, name='internal_dumpdata_view'),
    url(r'^data\.taggedtext$', internal_adobe_taggedtext_view, name='internal_adobe_taggedtext_view')
)
