from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import (
    tickets_address_view,
    tickets_confirm_view,
    tickets_thanks_view,
    tickets_tickets_view,
    tickets_welcome_view,
)


urlpatterns = patterns('',
    url(r'^$', tickets_welcome_view, dict(event_slug='tracon9'), name="tickets_welcome_view"),
    url(r'^products/?$', tickets_tickets_view, dict(event_slug='tracon9'), name="tickets_tickets_view"),
    url(r'^address/?$', tickets_address_view, dict(event_slug='tracon9'), name="tickets_address_view"),
    url(r'^confirm/?$', tickets_confirm_view, dict(event_slug='tracon9'), name="tickets_confirm_view"),
    url(r'^thanks/?$', tickets_thanks_view, dict(event_slug='tracon9'), name="tickets_thanks_view"),    
    url(r'', include('turska.urls')), 
)
