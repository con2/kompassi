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

# XXX * imports
from .models import *
from .forms import *
from .helpers import *
from .utils import *


__all__ = [
    "welcome_view",
    "tickets_view",
    "address_view",
    "confirm_view",
    "thanks_view",
    "ALL_PHASES",
    "manage_view",
    "stats_view",
    "payments_view",
    "process_single_payment_view",
    "confirm_single_payment_view",
    "process_multiple_payments_view",
    "confirm_multiple_payments_view",
    "create_batch_view",
    "render_batch_view",
    "cancel_batch_view",
    "deliver_batch_view",
    "search_view",
    "closed_view",
    "order_view",
    "tickets_by_date_view",
]


FIRST_PHASE = "welcome_phase"
LAST_PHASE = "thanks_phase"
EXIT_URL = settings.EVENT_URL


def multiform_validate(forms):
    return ["syntax"] if not all(
        i.is_valid() and (i.instance.target.available or i.cleaned_data["count"] == 0)
        for i in forms
    ) else []


def multiform_save(forms):
    return [i.save() for i in forms]


class Phase(object):
    name = "XXX_fill_me_in"
    friendly_name = "XXX Fill Me In"
    methods = ["GET", "POST"]
    template = "tickets/dummy.html"
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
        return init_form(NullForm, request, instance=None)

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
    template = "tickets/welcome.jade"
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


welcome_view = WelcomePhase()


class TicketsPhase(Phase):
    name = "tickets_phase"
    friendly_name = "Liput"
    template = "tickets/tickets.jade"
    prev_phase = "welcome_phase"
    next_phase = "address_phase"

    def make_form(self, request, event):
        order = get_order(request, event)
        forms = []

        # XXX When the admin changes the available property of products, existing sessions in the Tickets phase will break.
        for product in Product.objects.filter(available=True):
            order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
            form = init_form(OrderProductForm, request, instance=order_product, prefix="o%d" % order_product.pk)
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
    template = "tickets/address.jade"
    prev_phase = "tickets_phase"
    next_phase = "confirm_phase"

    def make_form(self, request, event):
        order = get_order(request, event)

        return init_form(CustomerForm, request, instance=order.customer)

    def save(self, request, form):
        order = get_order(request, event)
        cust = form.save()

        order.customer = cust
        order.save()


address_view = AddressPhase()


class ConfirmPhase(Phase):
    name = "confirm_phase"
    friendly_name = "Vahvistaminen"
    template = "tickets/confirm.jade"
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


confirm_view = ConfirmPhase()


class ThanksPhase(Phase):
    name = "thanks_phase"
    friendly_name = "Kiitos!"
    template = "tickets/thanks.jade"
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
    template = "tickets/closed.html"
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


thanks_view = ThanksPhase()
closed_view = ClosedPhase()


ALL_PHASES = [welcome_view, tickets_view, address_view, confirm_view, thanks_view]
for num, phase in enumerate(ALL_PHASES):
    phase.index = num


@ticket_admin_required
def manage_view(request, event):
    batches = event.batch_set.all()

    vars = dict(batches=batches)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/manage.html", vars, context_instance=context)


@ticket_admin_required
def stats_view(request, event):
    meta = event.tickets_event_meta

    confirmed_orders = event.order_set.filter(confirm_time__isnull=False)
    cancelled_orders = confirmed_orders.filter(cancellation_time__isnull=False)
    paid_orders = confirmed_orders.filter(cancellation_time__isnull=True, payment_date__isnull=False)
    delivered_orders = paid_orders.filter(batch__delivery_time__isnull=False)

    req_delivery = confirmed_orders.filter(order_product_set__product__requires_shipping=True).distinct()
    num_req_delivery = req_delivery.count()
    num_req_delivery_paid = req_delivery.filter(payment_date__isnull=False).count()
    shipping_and_handling_paid_cents = num_req_delivery_paid * meta.shipping_and_handling_cents
    shipping_and_handling_paid = format_price(shipping_and_handling_paid_cents)

    shipping_and_handling_total_cents = num_req_delivery * meta.shipping_and_handling_cents
    shipping_and_handling_total = format_price(shipping_and_handling_total_cents)

    data = []
    total_cents = 0
    total_paid_cents = 0

    for product in event.product_set.all():
        soldop_set = product.order_product_set.filter(order__confirm_time__isnull=False, order__cancellation_time__isnull=True)
        paidop_set = soldop_set.filter(order__payment_date__isnull=False)

        count = soldop_set.aggregate(count=Sum('count'))['count']
        count = count if count is not None else 0

        paid_count = paidop_set.aggregate(count=Sum('count'))['count']
        paid_count = paid_count if paid_count is not None else 0

        cents = count * product.price_cents
        total_cents += cents

        paid_cents = paid_count * product.price_cents
        total_paid_cents += paid_cents

        item = dict(product=product, count=count, cents=format_price(cents), paid_count=paid_count, paid_cents=format_price(paid_cents))
        data.append(item)

    total_cents += shipping_and_handling_total_cents
    total_paid_cents += shipping_and_handling_paid_cents

    total_price = format_price(total_cents)
    total_paid_price = format_price(total_paid_cents)

    vars = dict(
        data=data,
        num_confirmed_orders=confirmed_orders.count(),
        num_cancelled_orders=cancelled_orders.count(),
        num_paid_orders=paid_orders.count(),
        num_delivered_orders=delivered_orders.count(),
        num_req_delivery=num_req_delivery,
        num_req_delivery_paid=num_req_delivery_paid,
        shipping_and_handling_total=shipping_and_handling_total,
        shipping_and_handling_paid=shipping_and_handling_paid,

        total_price=total_price,
        total_paid_price=total_paid_price
    )
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/stats.html", vars, context_instance=context)

@login_required
def tickets_by_date_view(request, raw=False):
    confirmed_orders = Order.objects.filter(confirm_time__isnull=False, cancellation_time__isnull=True, order_product_set__product__name__contains='lippu').distinct()
    tickets_by_date = defaultdict(int)

    for order in confirmed_orders:
        date = order.confirm_time.date()
        for op in order.order_product_set.filter(product__name__contains='lippu').distinct():
            tickets_by_date[date] += op.count

    min_date = min(tickets_by_date.keys())
    max_date = max(tickets_by_date.keys())

    cur_date = min_date

    tsv = list()

    while cur_date <= max_date:
        tickets = tickets_by_date[cur_date]
        tsv.append("%s\t%s" % (cur_date.isoformat(), tickets))

        cur_date += datetime.timedelta(1)

    tsv = "\n".join(tsv)

    if raw:
        response = HttpResponse(tsv, content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename=tickets_by_date.tsv'
        return response
    else:
        vars = dict(tsv=tsv)
        context = RequestContext(request, {})
        return render_to_response("ticket_admin/tickets_by_date.html", vars, context_instance=context)

@ticket_admin_required
@require_GET
def payments_view(request, event):
    vars = dict(
        single_form=SinglePaymentForm(),
        multiple_form=MultiplePaymentsForm()
    )
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/payments.html", vars, context_instance=context)

@ticket_admin_required
@require_POST
def process_single_payment_view(request, event):
    form = SinglePaymentForm(request.POST)
    if not form.is_valid():
        return admin_error_page(request, u"Tarkista syöte.")

    try:
        order = get_order_by_ref(form.cleaned_data["ref_number"])
    except Order.DoesNotExist:
        return admin_error_page(request, u"Annetulla viitenumerolla ei löydy tilausta.")
    if not order.is_confirmed:
        return admin_error_page(request, u"Viitenumeroa vastaavaa tilausta ei ole vahvistettu.")
    if order.is_paid:
        return admin_error_page(request, u"Tilaus on jo merkitty maksetuksi %s." % format_date(order.payment_date))

    vars = dict(order=order)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/review_single.html", vars, context_instance=context)

@ticket_admin_required
@require_POST
def confirm_single_payment_view(request, event):
    form = ConfirmSinglePaymentForm(request.POST)
    if not form.is_valid():
        return admin_error_page(request, u"Jotain hämärää yritetty!")

    order = get_object_or_404(Order, id=form.cleaned_data["order_id"])
    order.confirm_payment(date.today())

    vars = dict(order=order)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/single_payment_ok.html", vars, context_instance=context)

@ticket_admin_required
@require_POST
def process_multiple_payments_view(request, event):
    form = MultiplePaymentsForm(request.POST)
    if not form.is_valid():
        return admin_error_page(request, u"Älä pliis jätä sitä pastee tähän -kenttää tyhjäks.")

    dump = form.cleaned_data["dump"]
    lines = dump.split("\n")
    payments = list(parse_payments(lines))

    vars = dict(payments=payments, dump=dump)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/review_multiple.html", vars, context_instance=context)

@ticket_admin_required
@require_POST
def confirm_multiple_payments_view(request, event):
    form = MultiplePaymentsForm(request.POST)
    if not form.is_valid():
        return admin_error_page(request, u"Jotain hämärää yritetty!")

    dump = form.cleaned_data["dump"]
    lines = dump.split("\n")
    payments = list(parse_payments(lines))

    for line, result, date, order in payments:
        if result == ParseResult.OK:
            order.confirm_payment(date)

    vars = dict(payments=payments)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/multiple_payments_ok.html", vars, context_instance=context)

@ticket_admin_required
@require_http_methods(["POST", "GET"])
def create_batch_view(request, event):
    if request.method == "POST":
        form = CreateBatchForm(request.POST)
        if form.is_valid():
            batch = Batch.create(max_orders=form.cleaned_data["max_orders"])

            vars = dict(batch=batch)
            context = RequestContext(request, {})
            return render_to_response("ticket_admin/create_batch_ok.html", vars, context_instance=context)
    else:
        form = CreateBatchForm()

    vars = dict(form=form)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/create_batch.html", vars, context_instance=context)

@ticket_admin_required
@require_GET
def render_batch_view(request, event, batch_id):
    batch = get_object_or_404(Batch, id=int(batch_id), event=event)

    response = HttpResponse(mimetype="application/pdf")
    response["Content-Disposition"] = 'filename=batch%03d.pdf' % batch.id
    c = canvas.Canvas(response)
    batch.render(c)
    c.save()

    return response

@ticket_admin_required
@require_http_methods(["POST", "GET"])
def cancel_batch_view(request, event, batch_id):
    batch = get_object_or_404(Batch, id=int(batch_id), event=event)

    if request.method == "POST":
        batch.cancel()

        vars = dict()
        context = RequestContext(request, {})
        return render_to_response("ticket_admin/cancel_batch_ok.html", vars, context_instance=context)

    else:
        vars = dict(batch=batch)
        context = RequestContext(request, {})
        return render_to_response("ticket_admin/cancel_batch.html", vars, context_instance=context)

@ticket_admin_required
@require_http_methods(["POST", "GET"])
def deliver_batch_view(request, event, batch_id):
    batch = get_object_or_404(Batch, id=int(batch_id), event=event)

    if batch.is_delivered:
        return admin_error_page(request, "Already delivered")

    vars = dict(batch=batch)
    context = RequestContext(request, {})

    if request.method == "POST":
        batch.confirm_delivery()

        return render_to_response("ticket_admin/deliver_batch_ok.html", vars, context_instance=context)

    else:
        return render_to_response("ticket_admin/deliver_batch.html", vars, context_instance=context)

@ticket_admin_required
@require_http_methods(["GET","POST"])
def search_view(request, event):
    orders = []

    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            orders = perform_search(**form.cleaned_data)
    else:
        form = SearchForm()
        orders =  Order.objects.filter(confirm_time__isnull=False).order_by('-confirm_time')
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    paginator = Paginator(orders, 100)
    try:
        orders = paginator.page(page)
    except (EmptyPage, InvalidPage):
        orders = paginator.page(paginator.num_pages)
    vars = dict(orders=orders, form=form)
    context = RequestContext(request, {})

    return render_to_response("ticket_admin/browse_orders.html", vars, context_instance=context)

@ticket_admin_required
@require_http_methods(["GET","POST"])
def order_view(request, event):
    try:
        orderid = int(request.GET.get('id', '1'))
    except ValueError:
        orderid = 0

    products = []
    order = get_object_or_404(Order, id=orderid)

    try:
        cancel = int(request.GET.get('cancel', '0'))
    except ValueError:
        cancel = 0

    if (order.id and cancel == 1):
        if (not order.cancellation_time):
            order.cancel()
        else:
            order.cancellation_time = None
            order.save()
        return HttpResponseRedirect(reverse('order_view') + '?id=' + str(order.id))

    try:
        payment = int(request.GET.get('payment', '0'))
    except ValueError:
        payment = 0

    if (order.id and payment == 1 and not order.cancellation_time):
        if (not order.payment_date):
            order.confirm_payment(date.today())
        else:
            order.payment_date = None
            order.save()
        return HttpResponseRedirect(reverse('order_view') + '?id=' + str(order.id))

    try:
        email = int(request.GET.get('email', '0'))
    except ValueError:
        email = 0

    if (order.id and email == 1 and not order.cancellation_time):
        order.send_confirmation_message("tilausvahvistus")
        return HttpResponseRedirect(reverse('order_view') + '?id=' + str(order.id))

    try:
        email = int(request.GET.get('email_payment', '0'))
    except ValueError:
        email = 0

    if (order.id and email == 1 and not order.cancellation_time and order.payment_date):
        order.send_confirmation_message("maksuvahvistus")
        return HttpResponseRedirect(reverse('order_view') + '?id=' + str(order.id))

    context = RequestContext(request, {})
    customer = init_form(CustomerForm, request, instance=order.customer, prefix="cust")

    for product in OrderProduct.objects.filter(order=order).order_by("id"):
        form = init_form(OrderProductForm, request, instance=product, prefix="o%d" % product.pk)
        products.append(form)

    vars = dict(order=order, customer=customer, products=products)

    return render_to_response("ticket_admin/order_view.html", vars, context_instance=context)

def admin_error_page(request, error):
    vars = dict(error=error)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/error.html", vars, context_instance=context)
