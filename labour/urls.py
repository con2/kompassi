from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import *

urlpatterns = patterns('',
    url(r'^event/(?P<event>[a-z0-9-]+)/signup$', labour_signup_view, name='labour_signup_view'),
)
