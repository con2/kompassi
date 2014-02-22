# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from tickets.views import *

urlpatterns = patterns('',
    url(r'events/(?P<event>[a-z0-9-]+)/tickets$', welcome_view, name="welcome_phase"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/products$', tickets_view, name="tickets_phase"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/delivery$', address_view, name="address_phase"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/confirm$', confirm_view, name="confirm_phase"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/thanks$', thanks_view, name="thanks_phase"),

    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin$', manage_view, name="manage_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/search$', search_view, name="search_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/orders$', order_view, name="order_view"),

    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/payments$', payments_view, name="payments_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/payments/single$', process_single_payment_view, name="process_single_payment_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/payments/single/confirm$', confirm_single_payment_view, name="confirm_single_payment_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/payments/multiple$', process_multiple_payments_view, name="process_multiple_payments_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/payments/multiple/confirm$', confirm_multiple_payments_view, name="confirm_multiple_payments_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/batches/new', name="create_batch_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)/$', render_batch_view, name="render_batch_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)/cancel$', cancel_batch_view, name="cancel_batch_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/batches/(?P<batch_id>\d+)/confirm$', deliver_batch_view, name="deliver_batch_view"),

    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/stats$', stats_view, name="stats_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/stats/by-date$', tickets_by_date_view, {'raw': False}, name="tickets_by_date_view"),
    url(r'events/(?P<event>[a-z0-9-]+)/tickets/admin/stats/by-date/raw$', tickets_by_date_view, {'raw': True}, name="tickets_by_date_raw"),
)
