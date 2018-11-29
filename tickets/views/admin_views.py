import datetime
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum, Q, Case, When, IntegerField
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_safe, require_http_methods
from django.views.decorators.csrf import csrf_exempt

from csp.decorators import csp_exempt

try:
    from reportlab.pdfgen import canvas
except ImportError:
    from warnings import warn
    warn('Failed to import ReportLab. Generating receipts will fail.')

from core.batches_view import batches_view
from core.csv_export import csv_response, CSV_EXPORT_FORMATS, EXPORT_FORMATS
from core.utils import url, initialize_form, slugify, login_redirect
from event_log.utils import emit

from ..forms import (
    AccommodationInformationForm,
    AdminOrderForm,
    CreateBatchForm,
    CustomerForm,
    OrderProductForm,
    SearchForm,
)
from ..helpers import tickets_admin_required, tickets_event_required, perform_search
from ..utils import format_price
from ..models import (
    AccommodationInformation,
    Batch,
    LimitGroup,
    Order,
    ShirtOrder,
    ShirtSize,
    UNPAID_CANCEL_HOURS,
)


__all__ = [
    "tickets_admin_batch_view",
    "tickets_admin_batches_view",
    "tickets_admin_menu_items",
    "tickets_admin_order_view",
    "tickets_admin_orders_view",
    "tickets_admin_stats_by_date_view",
    "tickets_admin_stats_view",
]


tickets_admin_batches_view = tickets_admin_required(batches_view(
    Batch=Batch,
    CreateBatchForm=CreateBatchForm,
    template="tickets_admin_batches_view.pug",
    created_at_field='create_time',
))


@tickets_admin_required
@require_safe
def tickets_admin_batch_view(request, vars, event, batch_id):
    batch = get_object_or_404(Batch, id=int(batch_id), event=event)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename=batch%03d.pdf' % batch.id
    c = canvas.Canvas(response)
    batch.render(c)
    c.save()

    return response


@tickets_admin_required
def tickets_admin_stats_view(request, vars, event):
    meta = event.tickets_event_meta

    confirmed_orders = event.order_set.filter(confirm_time__isnull=False)
    cancelled_orders = confirmed_orders.filter(cancellation_time__isnull=False)
    paid_orders = confirmed_orders.filter(cancellation_time__isnull=True, payment_date__isnull=False)
    delivered_orders = paid_orders.filter(batch__delivery_time__isnull=False)

    req_delivery = confirmed_orders.filter(cancellation_time__isnull=True, order_product_set__product__requires_shipping=True).distinct()
    num_req_delivery = req_delivery.count()
    num_req_delivery_paid = paid_orders.filter(order_product_set__product__requires_shipping=True).distinct().count()
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

    vars.update(
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

    return render(request, "tickets_admin_stats_view.pug", vars)


@tickets_admin_required
def tickets_admin_stats_by_date_view(request, vars, event, raw=False):
    confirmed_orders = event.order_set.filter(confirm_time__isnull=False, cancellation_time__isnull=True, order_product_set__product__name__contains='lippu').distinct()
    tickets_by_date = defaultdict(int)

    for order in confirmed_orders:
        date = order.confirm_time.date()

        # XXX this deserves an "XXX"
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
        vars.update(tsv=tsv)
        return render(request, "tickets_admin_stats_by_date_view.html", vars)


@tickets_admin_required
@require_http_methods(["GET","POST"])
def tickets_admin_orders_view(request, vars, event):
    orders = []
    form = initialize_form(SearchForm, request)

    if request.method == "POST":
        if form.is_valid():
            orders = perform_search(event=event, **form.cleaned_data)
    else:
        orders = event.order_set.filter(confirm_time__isnull=False).order_by('-confirm_time')

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    paginator = Paginator(orders, 100)

    try:
        orders = paginator.page(page)
    except (EmptyPage, InvalidPage):
        orders = paginator.page(paginator.num_pages)

    vars.update(orders=orders, form=form)
    return render(request, 'tickets_admin_orders_view.pug', vars)


@tickets_admin_required
@require_http_methods(["GET", "POST"])
def tickets_admin_order_view(request, vars, event, order_id):
    order = get_object_or_404(Order, id=int(order_id), event=event)

    customer_form = initialize_form(CustomerForm, request,
        instance=order.customer,
        prefix='customer',
    )

    order_form = initialize_form(AdminOrderForm, request,
        instance=order,
        prefix='order',
        readonly=True,
    )

    order_product_forms = OrderProductForm.get_for_order(request, order, admin=True)

    can_mark_paid = order.is_confirmed and not order.is_paid and not order.is_cancelled
    can_resend = order.is_confirmed and order.is_paid and not order.is_cancelled
    can_cancel = order.is_confirmed and not order.is_cancelled
    can_uncancel = order.is_cancelled

    if request.method == 'POST':
        if customer_form.is_valid() and all(form.fields['count'].widget.attrs.get('readonly', False) or form.is_valid() for form in order_product_forms):
            def save():
                customer_form.save()
                for form in order_product_forms:
                    if form.fields['count'].widget.attrs.get('readonly', False):
                        continue

                    form.save()

                order.clean_up_order_products()

            if 'cancel' in request.POST and can_cancel:
                save()
                order.cancel()
                messages.success(request, 'Tilaus peruutettiin.')
                return redirect('tickets_admin_order_view', event.slug, order.pk)

            elif 'uncancel' in request.POST and can_uncancel:
                save()
                order.uncancel()
                messages.success(request, 'Tilaus palautettiin.')
                return redirect('tickets_admin_order_view', event.slug, order.pk)

            elif 'mark-paid' in request.POST and can_mark_paid:
                save()
                order.confirm_payment()
                messages.success(request, 'Tilaus merkittiin maksetuksi.')
                return redirect('tickets_admin_order_view', event.slug, order.pk)

            elif 'resend-confirmation' in request.POST and can_resend:
                save()
                order.send_confirmation_message('payment_confirmation')
                messages.success(request, 'Vahvistusviesti lähetettiin uudelleen.')
                return redirect('tickets_admin_order_view', event.slug, order.pk)

            elif 'save' in request.POST:
                save()
                messages.success(request, 'Muutokset tallennettiin.')

            else:
                messages.error(request, 'Tuntematon tai kielletty toiminto.')
        else:
            messages.error(request, 'Ole hyvä ja tarkista lomake.')

    vars.update(
        order=order,

        customer_form=customer_form,
        order_form=order_form,

        can_cancel=can_cancel,
        can_mark_paid=can_mark_paid,
        can_resend=can_resend,
        can_uncancel=can_uncancel,

        # XXX due to template being shared with public view, needs to be named "form"
        form=order_product_forms,
    )

    # Slightly abusing the core.person.view entry type as there is no Person.
    # But the context field provides enough clue.
    emit('core.person.viewed', request=request, event=event)

    return render(request, 'tickets_admin_order_view.pug', vars)


@tickets_admin_required
@require_safe
@csp_exempt
def tickets_admin_etickets_view(request, vars, event, order_id):
    order = get_object_or_404(Order, id=int(order_id), event=event)

    return HttpResponse(order.get_etickets_pdf(), content_type='application/pdf')


@tickets_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def tickets_admin_tools_view(request, vars, event):
    unpaid_cancel_hours = request.GET.get('hours', UNPAID_CANCEL_HOURS)
    try:
        unpaid_cancel_hours = int(unpaid_cancel_hours)
    except ValueError:
        return HttpResponse('invalid hours', status=400)

    if request.method == 'POST':
        if 'cancel-unpaid' in request.POST:
            num_cancelled_orders = Order.cancel_unpaid_orders(event=event, hours=unpaid_cancel_hours)
            messages.success(request,
                '{num_cancelled_orders} tilausta peruttiin.'.format(**locals())
            )
        else:
            messages.error(request, 'Tuntematon toiminto.')

        return redirect('tickets_admin_tools_view', event.slug)

    vars.update(
        unpaid_cancel_hours=unpaid_cancel_hours,
        num_unpaid_orders_to_cancel=Order.get_unpaid_orders_to_cancel(event, hours=unpaid_cancel_hours).count(),
    )

    return render(request, 'tickets_admin_tools_view.pug', vars)


@tickets_admin_required
@require_safe
def tickets_admin_accommodation_view(request, vars, event, limit_group_id=None):
    if limit_group_id is not None:
        limit_group_id = int(limit_group_id)
        limit_group = get_object_or_404(LimitGroup, id=limit_group_id, event=event)
        query = Q(
            # Belongs to the selected night and school
            limit_groups=limit_group,
        ) & (
            Q(
                # Accommodation information is manually added
                order_product__isnull=True
            ) | Q(
                # Order is confirmed
                order_product__order__confirm_time__isnull=False,

                # Order is paid
                order_product__order__payment_date__isnull=False,

                # Order is not cancelled
                order_product__order__cancellation_time__isnull=True,
            )
        )
        accommodees = AccommodationInformation.objects.filter(query).order_by('last_name', 'first_name')
        active_filter = limit_group
    else:
        accommodees = []
        active_filter = None

    format = request.GET.get('format', 'screen')

    if format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}-{active_filter}-{timestamp}.{format}".format(
            event=event,
            active_filter=slugify(limit_group.description),
            timestamp=now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        emit('core.person.exported', request=request, event=event)

        return csv_response(event, AccommodationInformation, accommodees, filename=filename, dialect=CSV_EXPORT_FORMATS[format])
    elif format == 'screen':
        filters = [
            (limit_group_id == lg.id, lg)
            for lg in LimitGroup.objects.filter(
                event=event,
                product__requires_accommodation_information=True,
            ).distinct()
        ]

        vars.update(
            accommodees=accommodees,
            active_filter=active_filter,
            filters=filters,
        )

        return render(request, 'tickets_admin_accommodation_view.pug', vars)
    else:
        raise NotImplementedError(format)


@tickets_admin_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def tickets_admin_accommodation_create_view(request, vars, event, limit_group_id):
    limit_group_id = int(limit_group_id)
    limit_group = get_object_or_404(LimitGroup, id=limit_group_id, event=event)

    form = initialize_form(AccommodationInformationForm, request)

    if request.method == 'POST':
        info = form.save()
        info.limit_groups = [limit_group]
        info.save()

        messages.success(request, 'Majoittuja lisättiin.')
        return redirect('tickets_admin_accommodation_filtered_view', event.slug, limit_group_id)

    vars.update(
        form=form,
        limit_group=limit_group,
    )

    return render(request, 'tickets_admin_accommodation_create_view.pug', vars)


@tickets_admin_required
@require_safe
def tickets_admin_shirts_view(request, vars, event, format='screen'):
    shirt_sizes = ShirtSize.objects.filter(type__event=event).annotate(count=Sum(
        Case(
            When(
                shirt_orders__order__confirm_time__isnull=False,
                shirt_orders__order__payment_date__isnull=False,
                shirt_orders__order__cancellation_time__isnull=True,
                then='shirt_orders__count'
            ),
            default=0,
            output_field=IntegerField(),
        ),
    )).filter(count__gt=0).order_by('type__id', 'id')

    shirt_orders = ShirtOrder.objects.filter(
        order__event=event,
        order__confirm_time__isnull=False,
        order__payment_date__isnull=False,
        order__cancellation_time__isnull=True,
    ).order_by('order__customer__last_name', 'order__customer__first_name', 'size__type__id', 'size__id')

    if format == 'screen':
        vars.update(
            export_formats=EXPORT_FORMATS,
            shirt_sizes=shirt_sizes,
            shirt_sizes_total=shirt_sizes.aggregate(Sum('count'))['count__sum'] or 0,
            shirt_orders=shirt_orders,
            shirt_orders_total=shirt_orders.aggregate(Sum('count'))['count__sum'] or 0,
        )

        return render(request, 'tickets_admin_shirts_view.pug', vars)
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_shirts_{timestamp}.{format}".format(
            event=event,
            timestamp=now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        return csv_response(event, ShirtOrder, shirt_orders,
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
            m2m_mode='comma_separated',
        )


if 'lippukala' in settings.INSTALLED_APPS:
    from lippukala.views import POSView
    lippukala_pos_view = POSView.as_view()

    @csrf_exempt
    @tickets_event_required
    def tickets_admin_pos_view(request, event):
        # XXX kala expects event filter via &event=foo; we specify it via /events/foo
        request.GET = request.GET.copy()
        request.GET['event'] = event.slug

        meta = event.tickets_event_meta
        if not meta:
            messages.error(request, "Tämä tapahtuma ei käytä Kompassia lipunmyyntiin.")
            return redirect('core_event_view', event.slug)

        if not meta.is_user_allowed_pos_access(request.user):
            return login_redirect(request)

        return lippukala_pos_view(request)


def tickets_admin_menu_items(request, event):
    stats_url = url('tickets_admin_stats_view', event.slug)
    stats_active = request.path == stats_url
    stats_text = "Myyntitilanne"

    orders_url = url('tickets_admin_orders_view', event.slug)
    orders_active = request.path.startswith(orders_url)
    orders_text = "Tilaukset"

    batches_url = url('tickets_admin_batches_view', event.slug)
    batches_active = request.path.startswith(batches_url)
    batches_text = "Toimituserät"

    accommodation_url = url('tickets_admin_accommodation_view', event.slug)
    accommodation_active = request.path.startswith(accommodation_url)
    accommodation_text = "Majoituslistat"

    tools_url = url('tickets_admin_tools_view', event.slug)
    tools_active = request.path.startswith(tools_url)
    tools_text = "Työkalut"

    shirts_url = url('tickets_admin_shirts_view', event.slug)
    shirts_active = request.path.startswith(shirts_url)
    shirts_text = 'Paidat'

    items = [
        (stats_active, stats_url, stats_text),
        (orders_active, orders_url, orders_text),
        (batches_active, batches_url, batches_text),
        (accommodation_active, accommodation_url, accommodation_text),
        (tools_active, tools_url, tools_text),
        (shirts_active, shirts_url, shirts_text),
    ]

    if 'lippukala' in settings.INSTALLED_APPS:
        pos_url = url('tickets_admin_pos_view', event.slug)
        pos_active = False
        pos_text = "Lipuntarkastus"

        items.extend([
            (pos_active, pos_url, pos_text),
        ])

    return items
