# encoding: utf-8

from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from tickets.helpers import get_order, tickets_event_required
from core.utils import url

from .models import Payment
from .forms import PaymentForm

class PaymentStatus:
    TIMEOUT = -3
    ABORTED = -2
    CANCELLED = -1

    OK = 2
    DELAYED = 3
    FROZEN = 6

    CANCELLED_STATUSES = [TIMEOUT, ABORTED, CANCELLED]

def please_contact(order, reason=u"Tapahtui virhe."):
    return (
        u"{reason} "
        u"Ole hyvä ja ota yhteyttä sähköpostiosoitteeseen {order.event.tickets_event_meta.plain_contact_email}. "
        u"Viestissäsi ilmoita tilausnumerosi #{order.pk:05d}."
        .format(**locals())
    )


@tickets_event_required
@require_GET
def payments_redirect_view(request, event):
        order = get_order(request, event)
        meta = event.payments_event_meta

        if not order.is_confirmed:
            messages.error(request, u'Ole hyvä ja tee tilauksesi ensin valmiiksi.')
            return redirect('tickets_confirm_view', event.slug)

        if order.is_paid:
            messages.error(request, u'Tilaus on jo maksettu. Klikkaa "Uusi tilaus", jos haluat tilata lisää lippuja.')
            return redirect('tickets_thanks_view', event.slug)

        vars = dict(
            order=order,
            checkout_mac=order.checkout_mac(request),
            checkout_return_url=order.checkout_return_url(request),
            checkout_merchant=meta.checkout_merchant,
            checkout_delivery_date=meta.checkout_delivery_date,
            CHECKOUT_PARAMS=settings.CHECKOUT_PARAMS,
        )

        return render(request, 'payments_redirect_view.jade', vars)


@tickets_event_required
@require_GET
def payments_process_view(request, event):
    order = get_order(request, event)
    event = order.event

    if not order.is_confirmed:
        messages.error(request, please_contact(order, u"Yritetty maksaa keskeneräinen tilaus."))
        return redirect('tickets_confirm_view', event.slug)

    if order.is_paid:
        messages.error(request, please_contact(order, u"Tilaus on jo maksettu."))
        return redirect('tickets_thanks_view', event.slug)

    try:
        payment_info = Payment(event=event)
        payment_info = PaymentForm(request.GET, instance=payment_info).save()
    except ValueError:
        messages.error(request, please_contact(order, u"Maksu epäonnistui."))
        return redirect('tickets_confirm_view', event.slug)

    if payment_info.STATUS in PaymentStatus.CANCELLED_STATUSES:
        messages.warning(request, u"Maksu peruttiin.")
        return redirect('tickets_confirm_view', event.slug)

    if payment_info.STATUS == PaymentStatus.OK:
        order.confirm_payment() # send_email=True
        return redirect('tickets_thanks_view', event.slug)
    else:
        # TODO open ticket in JIRA
        messages.error(request, please_contact(order, u"Emme saaneet maksuoperaattorilta vahvistusta maksustasi."))
        return redirect('tickets_thanks_view', event.slug)

