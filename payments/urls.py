# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

from payments.views import *

urlpatterns = patterns('',
    url(r'process/$', payment_view, name="payment_view")
)
