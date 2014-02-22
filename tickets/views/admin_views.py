# encoding: utf-8

import datetime
from time import mktime
from collections import defaultdict

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
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
from ..models import *
from ..forms import *
from ..helpers import *
from ..utils import *


__all__ = [
    "tickets_cancel_batch_view",
    "tickets_confirm_multiple_payments_view",
    "tickets_confirm_single_payment_view",
    "tickets_create_batch_view",
    "tickets_deliver_batch_view",
    "tickets_manage_view",
    "tickets_order_view",
    "tickets_payments_view",
    "tickets_process_multiple_payments_view",
    "tickets_process_single_payment_view",
    "tickets_render_batch_view",
    "tickets_search_view",
    "tickets_stats_view",
    "tickets_tickets_by_date_view",
    "tickets_tickets_view",
]



@ticket_admin_required
def tickets_manage_view(request, event):
    batches = event.batch_set.all()

    vars = dict(batches=batches)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/manage.html", vars, context_instance=context)


@ticket_admin_required
def tickets_stats_view(request, event):
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


@ticket_admin_required
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
def tickets_payments_view(request, event):
    vars = dict(
        single_form=SinglePaymentForm(),
        multiple_form=MultiplePaymentsForm()
    )
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/payments.html", vars, context_instance=context)


@ticket_admin_required
@require_POST
def tickets_process_single_payment_view(request, event):
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
def tickets_confirm_single_payment_view(request, event):
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
def tickets_process_multiple_payments_view(request, event):
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
def tickets_confirm_multiple_payments_view(request, event):
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
def tickets_create_batch_view(request, event):
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
def tickets_render_batch_view(request, event, batch_id):
    batch = get_object_or_404(Batch, id=int(batch_id), event=event)

    response = HttpResponse(mimetype="application/pdf")
    response["Content-Disposition"] = 'filename=batch%03d.pdf' % batch.id
    c = canvas.Canvas(response)
    batch.render(c)
    c.save()

    return response


@ticket_admin_required
@require_http_methods(["POST", "GET"])
def tickets_cancel_batch_view(request, event, batch_id):
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
def tickets_deliver_batch_view(request, event, batch_id):
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
def tickets_search_view(request, event):
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
def tickets_order_view(request, event):
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
        return HttpResponseRedirect(reverse('tickets_order_view') + '?id=' + str(order.id))

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
        return HttpResponseRedirect(reverse('tickets_order_view') + '?id=' + str(order.id))

    try:
        email = int(request.GET.get('email', '0'))
    except ValueError:
        email = 0

    if (order.id and email == 1 and not order.cancellation_time):
        order.send_confirmation_message("tilausvahvistus")
        return HttpResponseRedirect(reverse('tickets_order_view') + '?id=' + str(order.id))

    try:
        email = int(request.GET.get('email_payment', '0'))
    except ValueError:
        email = 0

    if (order.id and email == 1 and not order.cancellation_time and order.payment_date):
        order.send_confirmation_message("maksuvahvistus")
        return HttpResponseRedirect(reverse('tickets_order_view') + '?id=' + str(order.id))

    context = RequestContext(request, {})
    customer = initialize_form(CustomerForm, request, instance=order.customer, prefix="cust")

    for product in OrderProduct.objects.filter(order=order).order_by("id"):
        form = initialize_form(OrderProductForm, request, instance=product, prefix="o%d" % product.pk)
        products.append(form)

    vars = dict(order=order, customer=customer, products=products)

    return render_to_response("ticket_admin/tickets_order_view.html", vars, context_instance=context)


def admin_error_page(request, error):
    vars = dict(error=error)
    context = RequestContext(request, {})
    return render_to_response("ticket_admin/error.html", vars, context_instance=context)
