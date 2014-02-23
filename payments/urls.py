# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from payments.views import payments_process_view

urlpatterns = patterns('',
    url(r'events/(?P<event_id>[a-z0-9-]+)/payments/process$', payments_process_view, name="payments_process_view")
)
