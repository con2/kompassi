from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import *

urlpatterns = patterns('',
    url(r'^$', core_frontpage_view, name='core_frontpage_view'),
    url(r'^event/(?P<event>[a-z0-9-]+)$', core_event_view, name='core_event_view'),
)
