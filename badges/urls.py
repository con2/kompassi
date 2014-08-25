from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import (
    badges_admin_index_view,
    badges_admin_batches_view,
    badges_admin_batch_view,
)


urlpatterns = patterns(
    '',

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/?$',
        badges_admin_index_view,
        name='badges_admin_index_view'
    ),

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/badges/(?P<badge_filter>[a-z0-9-]+)/?$',
        badges_admin_index_view,
        name='badges_admin_filtered_view'
    ),    

    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/batches/?$',
        badges_admin_batches_view,
        name='badges_admin_batches_view'
    ),
    
    url(
        r'^events/(?P<event_slug>[a-z0-9-]+)/badges/admin/batches/(?P<batch_id>\d+)?$',
        badges_admin_batch_view,
        name='badges_admin_batch_view'
    ),
)