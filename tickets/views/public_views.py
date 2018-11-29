# encoding: utf-8



from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

from core.utils import groupby_strict, initialize_form, url

from ..forms import *
from ..helpers import *
# XXX * imports
from ..models import (
    OrderProduct,
    ShirtOrder,
    ShirtSize,
)
from ..utils import *


__all__ = [
    "ALL_PHASES",
    "tickets_accommodation_view",
    "tickets_address_view",
    "tickets_confirm_view",
    "tickets_thanks_view",
    "tickets_tickets_view",
    "tickets_welcome_view",
]


def multiform_validate(forms):
    return ["syntax"] if not all(
        i.is_valid() and (i.instance.target.available or i.cleaned_data["count"] == 0)
        for i in forms
    ) else []


def multiform_save(forms):
    return [i.save() for i in forms]


def decorate(view_obj):
    """
    Applying decorators to our makeshift class based views seems a bit tricky.
    Let's do the decorator dance in this helper instead.

    NB. can't use functools.wraps due to Phase not having a __name__.

    Usage:
    realized_phase = ClassBasedView()
    realized_view = decorate(realized_phase)
    """
    @tickets_event_required
    def wrapper(request, event, *args, **kwargs):
        return view_obj(request, event, *args, **kwargs)
    return wrapper


class Phase(object):
    name = "XXX_fill_me_in"
    friendly_name = "XXX Fill Me In"
    methods = ["GET", "POST"]
    template = "tickets_dummy_phase.html"
    prev_phase = None
    next_phase = None
    payment_phase = None
    can_cancel = True
    index = None
    delay_complete = False

    def __call__(self, request, event):
        if request.method not in self.methods:
            return HttpResponseNotAllowed(self.methods)

        order = get_order(request, event)

        if not self.available(request, event):
            if order.is_confirmed:
                if order.is_paid:
                    return redirect('tickets_thanks_view', event.slug)
                else:
                    return redirect('tickets_confirm_view', event.slug)
            else:
                return redirect('tickets_welcome_view', event.slug)

        form = self.make_form(request, event)
        errors = []

        if request.method == "POST":
            # Which button was clicked?
            action = request.POST.get("action", "cancel")

            # On "Cancel" there's no need to do form validation, just bail out
            # right away.
            if action == "cancel":
                return self.cancel(request, event)

            if action not in ("next", "prev"):
                # TODO the user is manipulating the POST data
                raise NotImplementedError("evil user")

            # Data validity is checked before even attempting save.
            errors = self.validate(request, event, form)

            if not errors:
                self.save(request, event, form)

                # The "Next" button should only proceed with valid data.
                if action == "next":
                    if not self.delay_complete:
                        complete_phase(request, event, self.name)

                    return self.next(request, event)

            # The "Previous" button should work regardless of form validity.
            if action == "prev":
                # Clear any nastygrams left behind by validate
                for message in messages.get_messages(request):
                    pass

                return self.prev(request, event)

        # POST with invalid data and GET are handled the same.
        return self.get(request, event, form, errors)

    def available(self, request, event):
        order = get_order(request, event)
        return is_phase_completed(request, event, self.prev_phase) and not order.is_confirmed

    def validate(self, request, event, form):
        if not form.is_valid():
            messages.error(request, _('Please check the form.'))
            return ["syntax"]
        else:
            return []

    def get(self, request, event, form, errors):
        order = get_order(request, event)

        phases = []

        for phase in ALL_PHASES:
            phases.append(dict(
                url=url(phase.name, event.slug),
                friendly_name=phase.friendly_name,
                current=phase is self
            ))

        phase = dict(
            url=url(self.name, event.slug),
            next_phase=bool(self.next_phase),
            prev_phase=bool(self.prev_phase),
            can_cancel=self.can_cancel,
            can_go_back=self.can_go_back(request, event),
            payment_phase=self.payment_phase,
            name=self.name
        )

        vars = dict(self.vars(request, event, form),
            event=event,
            form=form,
            errors=errors,
            order=order,
            phase=phase,
            phases=phases,

            # XXX hack to hide the login form
            login_page=True
        )

        return render(request, self.template, vars)

    def make_form(self, request, event):
        return initialize_form(NullForm, request)

    def save(self, request, event, form):
        form.save()

    def next(self, request, event):
        return redirect(self.next_phase, event.slug)

    def prev(self, request, event):
        return redirect(self.prev_phase, event.slug)

    def cancel(self, request, event):
        destroy_order(request, event)
        return HttpResponseRedirect(event.homepage_url)

    def vars(self, request, event, form):
        return {}

    def can_go_back(self, request, event):
        return self.prev_phase is not None


class WelcomePhase(Phase):
    name = "tickets_welcome_view"
    friendly_name = _('Welcome')
    template = "tickets_welcome_phase.pug"
    prev_phase = None
    next_phase = "tickets_tickets_view"
    permit_new = True

    def save(self, request, event, form):
        order = get_order(request, event)
        order.save()
        set_order(request, event, order)

    def available(self, request, event):
        order = get_order(request, event)
        return not order.is_confirmed


tickets_welcome_phase = WelcomePhase()
tickets_welcome_view = decorate(tickets_welcome_phase)


class TicketsPhase(Phase):
    name = "tickets_tickets_view"
    friendly_name = _('Tickets')
    template = "tickets_tickets_phase.pug"
    prev_phase = "tickets_welcome_view"
    next_phase = "tickets_address_view"

    def make_form(self, request, event):
        order = get_order(request, event)
        return OrderProductForm.get_for_order(request, order)

    def validate(self, request, event, form):
        errors = multiform_validate(form)

        # If the above step failed, not all forms have cleaned_data.
        if errors:
            messages.error(request, _('Please check the form.'))
            return errors

        if sum(i.cleaned_data["count"] for i in form) <= 0:
            messages.info(request, _('Please select at least one product.'))
            errors.append("zero")
            return errors

        if any(i.instance.product.amount_available < i.cleaned_data["count"] for i in form):
            messages.error(request, _('Unfortunately a product you have selected has just been sold out.'))
            errors.append("soldout")
            return errors

        return []

    def save(self, request, event, form):
        multiform_save(form)

    def next(self, request, event):
        order = get_order(request, event)

        if order.t_shirts > 0:
            return redirect('tickets_shirts_view', event.slug)
        elif order.requires_accommodation_information:
            return redirect('tickets_accommodation_view', event.slug)
        else:
            return redirect(self.next_phase, event.slug)



tickets_tickets_phase = TicketsPhase()
tickets_tickets_view = decorate(tickets_tickets_phase)


class AccommodationPhase(Phase):
    name = "tickets_accommodation_view"
    friendly_name = _('Additional info')
    template = "tickets_accommodation_phase.pug"
    prev_phase = "tickets_tickets_view"
    next_phase = "tickets_address_view"

    def available(self, request, event):
        order = get_order(request, event)
        return order.requires_accommodation_information and not order.is_confirmed

    def validate(self, request, event, form):
        errors = ['syntax'] if not all(i.is_valid() for i in form) else []

        # If the above step failed, not all forms have cleaned_data.
        if errors:
            messages.error(request, _('Please check the form.'))
            return errors

    def make_form(self, request, event):
        order = get_order(request, event)
        return AccommodationInformationForm.get_for_order(request, order)

    def save(self, request, event, form):
        forms = form
        for form in forms:
            info = form.save()
            info.limit_groups = info.order_product.product.limit_groups.all()
            info.save()

    def next(self, request, event):
        order = get_order(request, event)

        if order.t_shirts > 0:
            return redirect('tickets_shirts_view', event.slug)
        else:
            return redirect(self.next_phase, event.slug)


tickets_accommodation_phase = AccommodationPhase()
tickets_accommodation_view = decorate(tickets_accommodation_phase)


class ShirtsPhase(Phase):
    """
    Some events want to sell T-shirts in advance. This phase queries the customer for shirt sizes.
    This phase is only displayed if the order contains T-shirts (order.t_shirts > 0).
    """

    name = "tickets_shirts_view"
    friendly_name = _('Shirt sizes')
    template = "tickets_shirts_phase.html"
    next_phase = "tickets_address_view"
    prev_phase = "tickets_tickets_view"

    def _get_sizes(self, event, **kwargs):
        return groupby_strict(
            ShirtSize.objects.filter(type__event=event).order_by("id"),
            lambda ss: ss.type
        )

    def vars(self, request, event, form):
        order = get_order(request, event)
        num_shirts = order.t_shirts
        shirt_sizes_by_type = self._get_sizes(event)
        return dict(
            num_shirts=num_shirts,
            shirt_sizes_by_type=shirt_sizes_by_type,
        )

    def make_form(self, request, event):
        order = get_order(request, event)
        sizes_by_type = self._get_sizes(event)
        forms = []

        for shirt_type, shirt_sizes in sizes_by_type:
            for size in shirt_sizes:
                shirt_order, created = ShirtOrder.objects.get_or_create(order=order, size=size)
                form = initialize_form(ShirtOrderForm, request, instance=shirt_order, prefix="s%d" % shirt_order.pk)
                forms.append(form)

        return forms

    def validate(self, request, event, form):
        order = get_order(request, event)
        errors = multiform_validate(form)

        if errors:
            return errors

        if sum(i.cleaned_data["count"] for i in form) != order.t_shirts:
            errors.append("num_tshirts")

        return errors

    def save(self, request, event, form):
        multiform_save(form)

    def available(self, request, event):
        order = get_order(request, event)
        sup_available = super(ShirtsPhase, self).available(request, event)

        return sup_available and order.t_shirts > 0

    def prev(self, request, event):
        order = get_order(request, event)

        if order.requires_accommodation_information:
            return redirect('tickets_accommodation_view', event.slug)
        else:
            return redirect(self.prev_phase, event.slug)


tickets_shirts_phase = ShirtsPhase()
tickets_shirts_view = decorate(tickets_shirts_phase)


class AddressPhase(Phase):
    name = "tickets_address_view"
    friendly_name = _('Delivery address')
    template = "tickets_address_phase.pug"
    prev_phase = "tickets_tickets_view"
    next_phase = "tickets_confirm_view"

    def make_form(self, request, event):
        order = get_order(request, event)

        return initialize_form(CustomerForm, request, instance=order.customer)

    def save(self, request, event, form):
        order = get_order(request, event)
        cust = form.save()

        order.customer = cust
        order.save()

    def prev(self, request, event):
        order = get_order(request, event)

        if order.t_shirts > 0:
            return redirect('tickets_shirts_view', event.slug)
        if order.requires_accommodation_information:
            return redirect('tickets_accommodation_view', event.slug)
        else:
            return redirect(self.prev_phase, event.slug)


tickets_address_phase = AddressPhase()
tickets_address_view = decorate(tickets_address_phase)


class ConfirmPhase(Phase):
    name = "tickets_confirm_view"
    friendly_name = _('Confirmation')
    template = "tickets_confirm_phase.pug"
    prev_phase = "tickets_address_view"
    next_phase = "payments_redirect_view"
    payment_phase = True
    delay_complete = True

    def validate(self, request, event, form):
        errors = multiform_validate(form)
        order = get_order(request, event)
        order_products = order.order_product_set.filter(count__gt=0)

        if any(i.product.amount_available < i.count for i in order_products):
            messages.error(request, 'Valitsemasi tuote on valitettavasti juuri myyty loppuun.')
            errors.append("soldout_confirm")
            return errors

        return []

    def vars(self, request, event, form):
        order = get_order(request, event)
        products = order.order_product_set.filter(order=order, count__gt=0)

        return dict(
            products=products,
        )

    def available(self, request, event):
        order = get_order(request, event)
        return is_phase_completed(request, event, self.prev_phase) and not order.is_paid

    def save(self, request, event, form):
        order = get_order(request, event)
        action = request.POST.get("action", "cancel")

        if action == 'next' and not order.is_confirmed:
            order.confirm_order()

    def can_go_back(self, request, event):
        order = get_order(request, event)
        return not order.is_confirmed


tickets_confirm_phase = ConfirmPhase()
tickets_confirm_view = decorate(tickets_confirm_phase)


class ThanksPhase(Phase):
    name = "tickets_thanks_view"
    friendly_name = _('Thank you!')
    template = "tickets_thanks_phase.pug"
    prev_phase = None
    next_phase = "tickets_welcome_view"
    can_cancel = False

    def available(self, request, event):
        order = get_order(request, event)
        return order.is_confirmed and order.is_paid

    def vars(self, request, event, form):
        order = get_order(request, event)
        products = OrderProduct.objects.filter(order=order)

        return dict(products=products)

    def save(self, request, event, form):
        # Start a new order
        clear_order(request, event)


tickets_thanks_phase = ThanksPhase()
tickets_thanks_view = decorate(tickets_thanks_phase)


ALL_PHASES = [
    tickets_welcome_phase,
    tickets_tickets_phase,
    tickets_accommodation_phase,
    tickets_shirts_phase,
    tickets_address_phase,
    tickets_confirm_phase,
    tickets_thanks_phase,
]

for num, phase in enumerate(ALL_PHASES):
    phase.index = num


def tickets_event_box_context(request, event):
    if event.tickets_event_meta:
        is_tickets_admin = event.tickets_event_meta.is_user_admin(request.user)
    else:
        is_tickets_admin = False

    return dict(
        is_tickets_admin=is_tickets_admin
    )
