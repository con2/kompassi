from django.conf.urls import include, url
from payments.views import payments_process_view, payments_redirect_view

urlpatterns = [
    url(r'events/(?P<event_slug>[a-z0-9-]+)/payments/redirect$', payments_redirect_view, name="payments_redirect_view"),
    url(r'events/(?P<event_slug>[a-z0-9-]+)/payments/process$', payments_process_view, name="payments_process_view"),
]
