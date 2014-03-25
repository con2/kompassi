# encoding: utf-8

from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from .views import (
    tickets_address_view,
    tickets_admin_batch_cancel_view,
    tickets_admin_batch_create_view,
    tickets_admin_batch_deliver_view,
    tickets_admin_batch_view,
    tickets_admin_batches_view,
    tickets_admin_order_view,
    tickets_admin_orders_view,
    tickets_admin_stats_by_date_view,
    tickets_admin_stats_view,
    tickets_closed_view,
    tickets_confirm_view,
    tickets_thanks_view,
    tickets_tickets_view,
    tickets_welcome_view,
)


urlpatterns = patterns('',
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets$', tickets_welcome_view, name="tickets_welcome_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/products$', tickets_tickets_view, name="tickets_tickets_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/address$', tickets_address_view, name="tickets_address_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/confirm$', tickets_confirm_view, name="tickets_confirm_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/thanks$', tickets_thanks_view, name="tickets_thanks_view"),

    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin$', tickets_admin_stats_view, name="tickets_admin_stats_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/by-date/raw$', tickets_admin_stats_by_date_view, {'raw': True}, name="tickets_admin_stats_by_date_view"),

    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders$', tickets_admin_orders_view, name="tickets_admin_orders_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/orders/(?P<order_id>\d+)/$', tickets_admin_order_view, name="tickets_admin_order_view"),

    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches', tickets_admin_batches_view, name="tickets_admin_batches_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches/new', tickets_admin_batch_create_view, name="tickets_admin_batch_create_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)$', tickets_admin_batch_view, name="tickets_admin_batch_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)/cancel$', tickets_admin_batch_cancel_view, name="tickets_admin_batch_cancel_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)/deliver$', tickets_admin_batch_deliver_view, name="tickets_admin_batch_deliver_view"),

)
