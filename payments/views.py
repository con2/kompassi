# encoding: utf-8
# vim: shiftwidth=4 expandtab

from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.conf import settings
from django.contrib.messages import add_message, INFO, ERROR, WARNING
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

from tickets.helpers import get_order, tickets_event_required
from core.utils import url

from .forms import PaymentForm

# http://demo1.checkout.fi/xml2.php

# XXX where should this be defined?
class PaymentStatus:
  TIMEOUT = -3
  ABORTED = -2
  CANCELLED = -1

  OK = 2
  DELAYED = 3
  FROZEN = 6

  CANCELLED_STATUSES = [TIMEOUT, ABORTED, CANCELLED]

def please_contact(reason="Tapahtui virhe."):
  email = settings.DEFAULT_FROM_EMAIL
  return "{reason} Ole hyvä ja ota yhteyttä: {email}".format(**locals())

@tickets_event_required
@require_GET
def payments_process_view(request, event):
  order = get_order(request, event)
  event = order.event

  if not order.customer:
    add_message(request, ERROR, please_contact("Yritetty maksaa keskeneräinen tilaus."))
    return redirect('tickets_welcome_view', event.slug)

  if order.is_paid:
    add_message(request, ERROR, please_contact("Tilaus on jo maksettu."))

  try:
    payment_info = PaymentForm(request.GET).save()
  except ValueError:
    add_message(request, ERROR, please_contact("Maksu epäonnistui."))
    return redirect('tickets_confirm_view', event.slug)

  if payment_info.STATUS in PaymentStatus.CANCELLED_STATUSES:
    add_message(request, INFO, "Maksu peruttiin.") # XXX
    return redirect('tickets_confirm_view', event.slug)

  if payment_info.STATUS == PaymentStatus.OK:
    order.confirm_order(send_email=False)
    order.confirm_payment() # send_email=True
    return redirect('tickets_thanks_view', event.slug)
  else:
    order.confirm_order()
    add_message(request, WARNING, "Tilauksesi onnistui, mutta emme saaneet lopullista vahvistusta maksustasi. Saat erillisen maksuvahvistusviestin, kun maksusi on vahvistettu.")
    return redirect('tickets_thanks_view', event.slug)

def make_form(request):
  return initialize_form(PaymentForm, request, instance=None)
