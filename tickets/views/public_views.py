# encoding: utf-8

import datetime
from time import mktime
from collections import defaultdict

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages import add_message, INFO, WARNING, ERROR
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum

try:
    from reportlab.pdfgen import canvas
except ImportError:
    from warnings import warn
    warn('Failed to import ReportLab. Generating receipts will fail.')

from core.utils import multiform_validate, multiform_save

# XXX * imports
from ..models import *
from ..forms import *
from ..helpers import *
from ..utils import *


__all__ = [
    "ALL_PHASES",
    "tickets_address_view",
    "tickets_closed_view",
    "tickets_confirm_view",
    "tickets_thanks_view",
    "tickets_tickets_view",
    "tickets_welcome_view",
]


FIRST_PHASE = "welcome_phase"
LAST_PHASE = "thanks_phase"
EXIT_URL = settings.EVENT_URL


class Phase(object):
    name = "XXX_fill_me_in"
    friendly_name = "XXX Fill Me In"
    methods = ["GET", "POST"]
    template = "tickets_dummy_phase.html"
    prev_phase = None
    next_phase = None
    payment_phase = None
    next_text = "Seuraava &raquo;"
    can_cancel = True
    index = None

    @ticket_event_required
    def __call__(self, request, event):
        if request.method not in self.methods:
            return HttpResponseNotAllowed(self.methods)

        order = get_order(request, event)

        if not self.available(request):
            if order.is_confirmed:
                return redirect(LAST_PHASE)
            else:
                return redirect(FIRST_PHASE)

        form = self.make_form(request, event)

        if request.method == "POST":
            # Which button was clicked?
            action = request.POST.get("action", "cancel")

            # On "Cancel" there's no need to do form validation, just bail out
            # right away.
            if action == "cancel":
                return self.cancel(request)

            if action not in ("next", "prev"):
                # TODO the user is manipulating the POST data
                raise NotImplementedError("evil user")

            # Data validity is checked before even attempting save.
            errors = self.validate(request, form)

            if not errors:
                self.save(request, form)

                # The "Next" button should only proceed with valid data.
                if action == "next":
                    complete_phase(request, self.name)
                    return self.next(request)

            # The "Previous" button should work regardless of form validity.
            if action == "prev":
                return self.prev(request)

            # "Next" with invalid data falls through.
        elif request.method == "GET":
            if request.session.get('payment_status') == 2:
                del request.session['payment_status']
                if not order.is_confirmed:
                    order.confirm_order()
                    complete_phase(request, event, self.name)
                    return self.next(request)
                else:
                    return redirect("confirm_phase")
            else:
                errors = []
        else:
            errors = []

        # POST with invalid data and GET are handled the same.
        return self.get(request, form, errors)

    def available(self, request):
        order = get_order(request, event)
        return is_phase_completed(request, event, self.prev_phase) and not order.is_confirmed

    def validate(self, request, form):
        if not form.is_valid():
            add_message(request, ERROR, 'Tarkista lomakkeen sisältö.')
            return ["syntax"]
        else:
            return []

    def get(self, request, form, errors):
        order = get_order(request, event)

        context = RequestContext(request, {})
        phases = []

        for phase in ALL_PHASES:
            phases.append(dict(
                url=reverse(phase.name),
                friendly_name=phase.friendly_name,
                available=phase.index < self.index and not order.is_confirmed,
                current=phase is self
            ))

        phase = dict(
            url=reverse(self.name),
            next_phase=bool(self.next_phase),
            prev_phase=bool(self.prev_phase),
            can_cancel=self.can_cancel,
            next_text=self.next_text,
            payment_phase=self.payment_phase,
            name=self.name
        )

        vars = dict(self.vars(request, form), form=form, errors=errors, order=order, phase=phase, phases=phases)
        return render_to_response(self.template, vars, context_instance=context)

    def make_form(self, request, event):
        return initialize_form(NullForm, request, instance=None)

    def save(self, request, form):
        form.save()

    def next(self, request):
        return redirect(self.next_phase)

    def prev(self, request):
        return redirect(self.prev_phase)

    def cancel(self, request):
        destroy_order(request, event)
        return HttpResponseRedirect(EXIT_URL)

    def vars(self, request, form):
        return {}


class WelcomePhase(Phase):
    name = "welcome_phase"
    friendly_name = "Tervetuloa"
    template = "tickets_welcome_phase.jade"
    prev_phase = None
    next_phase = "tickets_phase"
    permit_new = True

    def save(self, request, form):
        order = get_order(request, event)
        order.save()
        set_order(request, event, order)

    def available(self, request):
        order = get_order(request, event)
        return not order.is_confirmed


tickets_welcome_view = WelcomePhase()


class TicketsPhase(Phase):
    name = "tickets_phase"
    friendly_name = "Liput"
    template = "tickets_tickets_phase.jade"
    prev_phase = "welcome_phase"
    next_phase = "address_phase"

    def make_form(self, request, event):
        order = get_order(request, event)
        forms = []

        # XXX When the admin changes the available property of products, existing sessions in the Tickets phase will break.
        for product in Product.objects.filter(available=True):
            order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
            form = initialize_form(OrderProductForm, request, instance=order_product, prefix="o%d" % order_product.pk)
            forms.append(form)

        return forms

    def validate(self, request, form):
        errors = multiform_validate(form)

        # If the above step failed, not all forms have cleaned_data.
        if errors:
            return errors

        if sum(i.cleaned_data["count"] for i in form) <= 0:
            add_message(request, INFO, 'Valitse vähintään yksi tuote.')
            errors.append("zero")
            return errors

        if (is_soldout(dict((i.instance.product, i.cleaned_data["count"]) for i in form))):
            add_message(request, ERROR, 'Valitsemasi tuote on valitettavasti juuri myyty loppuun.')
            errors.append("soldout")
            return errors

        return []

    def save(self, request, form):
        multiform_save(form)


tickets_view = TicketsPhase()


class AddressPhase(Phase):
    name = "address_phase"
    friendly_name = "Toimitusosoite"
    template = "tickets_address_phase.jade"
    prev_phase = "tickets_phase"
    next_phase = "confirm_phase"

    def make_form(self, request, event):
        order = get_order(request, event)

        return initialize_form(CustomerForm, request, instance=order.customer)

    def save(self, request, form):
        order = get_order(request, event)
        cust = form.save()

        order.customer = cust
        order.save()


tickets_address_view = AddressPhase()


class ConfirmPhase(Phase):
    name = "confirm_phase"
    friendly_name = "Vahvistaminen"
    template = "tickets_confirm_phase.jade"
    prev_phase = "address_phase"
    next_phase = "thanks_phase"
    payment_phase = True
    next_text ="Siirry maksamaan &#10003;"

    def validate(self, request, form):
        errors = multiform_validate(form)
        order = get_order(request, event)
        products = OrderProduct.objects.filter(order=order, count__gt=0)
        if (is_soldout(dict((i.product, i.count) for i in products))):
            errors.append("soldout_confirm")
            return errors
        return []

    def vars(self, request, form):
        order = get_order(request, event)
        products = OrderProduct.objects.filter(order=order, count__gt=0)

        return dict(products=products)

    def save(self, request, form):
        pass

    def next(self, request):
        order = get_order(request, event)
        # .confirm_* call .save
        if not order.is_confirmed:
            return HttpResponseRedirect("http://localhost:8000/process/?test=1")
        else:
            payment_phase = None
            return super(ConfirmPhase, self).next(request)


tickets_confirm_view = ConfirmPhase()


class ThanksPhase(Phase):
    name = "thanks_phase"
    friendly_name = "Kiitos!"
    template = "tickets_thanks_phase.jade"
    prev_phase = None
    next_phase = "welcome_phase"
    next_text = "Uusi tilaus"
    can_cancel = False

    def available(self, request):
        order = get_order(request, event)
        return order.is_confirmed

    def vars(self, request, form):
        order = get_order(request, event)
        products = OrderProduct.objects.filter(order=order)

        return dict(products=products)

    def save(self, request, form):
        pass

    def next(self, request):
        # Start a new order
        clear_order(request, event)

        return redirect(self.next_phase)


class ClosedPhase(Phase):
    name = "welcome_phase"
    friendly_name = "Tervetuloa!"
    template = "tickets_closed_phase.html"
    prev_phase = None
    next_phase = None
    can_cancel = True
    index = 0

    def available(self, request):
        return True

    def save(self, request, form):
        pass

    def next(self, request):
        return HttpResponseRedirect(settings.EVENT_URL)


tickets_thanks_view = ThanksPhase()
tickets_closed_view = ClosedPhase()


ALL_PHASES = [tickets_welcome_view, tickets_view, tickets_address_view, tickets_confirm_view, tickets_thanks_view]
for num, phase in enumerate(ALL_PHASES):
    phase.index = num
