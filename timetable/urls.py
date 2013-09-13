from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import *

urlpatterns = patterns('',
    url(r'^$', lambda req: redirect('/timetable'), name='frontpage_redirect_view'),
    url(r'^timetable$', timetable_view, name='timetable_view'),
    url(r'^m/timetable$', mobile_timetable_view, name='mobile_timetable_view'),
    url(r'^m/timetable/(\d{0,4})', mobile_programme_detail_view, name='mobile_programme_detail_view'),
    url(r'^extranet/timetable$', internal_timetable_view, name='internal_timetable_view'),
    url(r'^data\.json$', internal_dumpdata_view, name='internal_dumpdata_view'),
    url(r'^data\.taggedtext$', internal_adobe_taggedtext_view, name='internal_adobe_taggedtext_view')
)
