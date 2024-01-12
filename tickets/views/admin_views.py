import datetime
from collections import defaultdict

from csp.decorators import csp_exempt
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from lippukala.consts import BEYOND_LOGIC, MANUAL_INTERVENTION_REQUIRED
from lippukala.views import POSView

from core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, csv_response
from core.sort_and_filter import Filter
from core.utils import initialize_form, login_redirect, slugify, url
from event_log.utils import emit

from ..forms import (
    AccommodationInformationAdminForm,
    AccommodationPresenceForm,
    AdminOrderForm,
    CustomerForm,
    OrderProductForm,
    SearchForm,
)
from ..helpers import perform_search, tickets_admin_required, tickets_event_required
from ..models import (
    AccommodationInformation,
    LimitGroup,
    Order,
    OrderProduct,
)
from ..models.consts import UNPAID_CANCEL_HOURS
from ..utils import format_price

__all__ = [
    "tickets_admin_menu_items",
    "tickets_admin_order_view",
    "tickets_admin_orders_view",
    "tickets_admin_stats_by_date_view",
    "tickets_admin_stats_view",
]


@tickets_admin_required
def tickets_admin_stats_view(request, vars, event):
    meta = event.tickets_event_meta

    confirmed_orders = event.order_set.filter(confirm_time__isnull=False)
    cancelled_orders = confirmed_orders.filter(cancellation_time__isnull=False)
    paid_orders = confirmed_orders.filter(cancellation_time__isnull=True, payment_date__isnull=False)

    data = []
    total_cents = 0
    total_paid_cents = 0

    for product in event.product_set.all():
        soldop_set = product.order_product_set.filter(
            order__confirm_time__isnull=False, order__cancellation_time__isnull=True
        )
        paidop_set = soldop_set.filter(order__payment_date__isnull=False)

        count = soldop_set.aggregate(count=Sum("count"))["count"]
        count = count if count is not None else 0

        paid_count = paidop_set.aggregate(count=Sum("count"))["count"]
        paid_count = paid_count if paid_count is not None else 0

        cents = count * product.price_cents
        total_cents += cents

        paid_cents = paid_count * product.price_cents
        total_paid_cents += paid_cents

        item = dict(
            product=product,
            count=count,
            cents=format_price(cents),
            paid_count=paid_count,
            paid_cents=format_price(paid_cents),
        )
        data.append(item)

    total_price = format_price(total_cents)
    total_paid_price = format_price(total_paid_cents)

    vars.update(
        data=data,
        num_confirmed_orders=confirmed_orders.count(),
        num_cancelled_orders=cancelled_orders.count(),
        num_paid_orders=paid_orders.count(),
        total_price=total_price,
        total_paid_price=total_paid_price,
    )

    return render(request, "tickets_admin_stats_view.pug", vars)


@tickets_admin_required
def tickets_admin_stats_by_date_view(request, vars, event, raw=False):
    confirmed_orders = event.order_set.filter(
        confirm_time__isnull=False,
        cancellation_time__isnull=True,
        order_product_set__product__name__contains="lippu",
    ).distinct()
    tickets_by_date = defaultdict(int)

    for order in confirmed_orders:
        date = order.confirm_time.date()

        # XXX this deserves an "XXX"
        for op in order.order_product_set.filter(product__name__contains="lippu").distinct():
            tickets_by_date[date] += op.count

    min_date = min(tickets_by_date.keys())
    max_date = max(tickets_by_date.keys())

    cur_date = min_date

    tsv = list()

    while cur_date <= max_date:
        tickets = tickets_by_date[cur_date]
        tsv.append(f"{cur_date.isoformat()}\t{tickets}")

        cur_date += datetime.timedelta(1)

    tsv = "\n".join(tsv)

    if raw:
        response = HttpResponse(tsv, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=tickets_by_date.tsv"
        return response
    else:
        vars.update(tsv=tsv)
        return render(request, "tickets_admin_stats_by_date_view.html", vars)


@tickets_admin_required
@require_http_methods(["GET", "POST"])
def tickets_admin_orders_view(request, vars, event):
    orders = []
    form = initialize_form(SearchForm, request)

    if request.method == "POST":
        if form.is_valid():
            orders = perform_search(event=event, **form.cleaned_data)
    else:
        orders = event.order_set.filter(confirm_time__isnull=False).order_by("-confirm_time")

    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1

    paginator = Paginator(orders, 100)

    try:
        orders = paginator.page(page)
    except (EmptyPage, InvalidPage):
        orders = paginator.page(paginator.num_pages)

    vars.update(orders=orders, form=form)
    return render(request, "tickets_admin_orders_view.pug", vars)


@tickets_admin_required
@require_http_methods(["GET", "POST"])
def tickets_admin_order_view(request, vars, event, order_id):
    order = get_object_or_404(Order, id=int(order_id), event=event)

    customer_form = initialize_form(
        CustomerForm,
        request,
        instance=order.customer,
        order=order,
        prefix="customer",
    )

    order_form = initialize_form(
        AdminOrderForm,
        request,
        instance=order,
        prefix="order",
        readonly=True,
    )

    order_product_forms = OrderProductForm.get_for_order(request, order, admin=True)

    can_mark_paid = order.is_confirmed and not order.is_paid and not order.is_cancelled
    can_resend = order.is_confirmed and order.is_paid and not order.is_cancelled
    can_cancel = order.is_confirmed and not order.is_cancelled
    can_uncancel = order.is_cancelled

    if request.method == "POST":
        if customer_form.is_valid() and all(
            form.fields["count"].widget.attrs.get("readonly", False) or form.is_valid() for form in order_product_forms
        ):

            def save():
                customer_form.save()
                for form in order_product_forms:
                    if form.fields["count"].widget.attrs.get("readonly", False):
                        continue

                    form.save()

                order.clean_up_order_products()

            if "cancel" in request.POST and can_cancel:
                save()
                order.cancel()
                messages.success(request, "Tilaus peruutettiin.")
                return redirect("tickets_admin_order_view", event.slug, order.pk)

            elif "uncancel" in request.POST and can_uncancel:
                save()
                order.uncancel()
                messages.success(request, "Tilaus palautettiin.")
                return redirect("tickets_admin_order_view", event.slug, order.pk)

            elif "mark-paid" in request.POST and can_mark_paid:
                save()
                order.confirm_payment()
                messages.success(request, "Tilaus merkittiin maksetuksi.")
                return redirect("tickets_admin_order_view", event.slug, order.pk)

            elif "resend-confirmation" in request.POST and can_resend:
                save()
                order.send_confirmation_message("payment_confirmation")
                messages.success(request, "Vahvistusviesti lähetettiin uudelleen.")
                return redirect("tickets_admin_order_view", event.slug, order.pk)

            elif "save" in request.POST:
                save()
                messages.success(request, "Muutokset tallennettiin.")

            else:
                messages.error(request, "Tuntematon tai kielletty toiminto.")
        else:
            messages.error(request, "Ole hyvä ja tarkista lomake.")

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
        admin=True,
    )

    # Slightly abusing the core.person.view entry type as there is no Person.
    # But the context field provides enough clue.
    emit("core.person.viewed", request=request, event=event)

    return render(request, "tickets_admin_order_view.pug", vars)


@tickets_admin_required
@require_safe
@csp_exempt
def tickets_admin_etickets_view(request, vars, event, order_id):
    order = get_object_or_404(Order, id=int(order_id), event=event)

    return HttpResponse(order.get_etickets_pdf(), content_type="application/pdf")


@tickets_admin_required
@require_http_methods(["GET", "HEAD", "POST"])
def tickets_admin_tools_view(request, vars, event):
    unpaid_cancel_hours = request.GET.get("hours", UNPAID_CANCEL_HOURS)
    try:
        unpaid_cancel_hours = int(unpaid_cancel_hours)
    except ValueError:
        return HttpResponse("invalid hours", status=400)

    if request.method == "POST":
        if "cancel-unpaid" in request.POST:
            num_cancelled_orders = Order.cancel_unpaid_orders(event=event, hours=unpaid_cancel_hours)
            messages.success(request, f"{num_cancelled_orders} tilausta peruttiin.")
        else:
            messages.error(request, "Tuntematon toiminto.")

        return redirect("tickets_admin_tools_view", event.slug)

    vars.update(
        unpaid_cancel_hours=unpaid_cancel_hours,
        num_unpaid_orders_to_cancel=Order.get_unpaid_orders_to_cancel(event, hours=unpaid_cancel_hours).count(),
    )

    return render(request, "tickets_admin_tools_view.pug", vars)


@tickets_event_required
@require_http_methods(["GET", "HEAD", "POST"])
def tickets_admin_accommodation_view(request, event, limit_group_id=None):
    if not event.tickets_event_meta.is_user_allowed_accommodation_access(request.user):
        raise PermissionDenied()

    vars = dict(event=event)

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
            )
            | Q(
                # Order is confirmed
                order_product__order__confirm_time__isnull=False,
                # Order is paid
                order_product__order__payment_date__isnull=False,
                # Order is not cancelled
                order_product__order__cancellation_time__isnull=True,
            )
        )
        accommodees = AccommodationInformation.objects.filter(query).order_by("last_name", "first_name")
        active_filter = limit_group
    else:
        accommodees = AccommodationInformation.objects.none()
        active_filter = None
        limit_group = None

    present_filter = Filter(request, "state").add_choices(
        "state",
        AccommodationInformation.State.choices,
    )
    accommodees = present_filter.filter_queryset(accommodees)

    format = request.GET.get("format", "screen")

    if format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}-{active_filter}-{timestamp}.{format}".format(
            event=event,
            active_filter=slugify(limit_group.description) if limit_group else "tickets",
            timestamp=now().strftime("%Y%m%d%H%M%S"),
            format=format,
        )

        emit("core.person.exported", request=request, event=event)

        return csv_response(
            event,
            AccommodationInformation,
            accommodees,
            filename=filename,
            dialect=CSV_EXPORT_FORMATS[format],
        )
    elif format == "screen":
        # ticket shoppe limit grouppes that have accommodation products
        q = Q(
            event=event,
            product__requires_accommodation_information=True,
        )

        # shortcut: limit grouppes that already have accommodees
        # required for labour accommodation
        q |= Q(
            event=event,
            accommodation_information_set__isnull=False,
        )

        filters = [(limit_group_id == lg.id, lg) for lg in LimitGroup.objects.filter(q).distinct().order_by("id")]

        vars.update(
            accommodees=accommodees,
            present_filter=present_filter,
            # TODO legacy manual filter
            active_filter=active_filter,
            limit_group=limit_group,
            filters=filters,
        )

        return render(request, "tickets_admin_accommodation_view.pug", vars)
    else:
        raise NotImplementedError(format)


@tickets_event_required
@require_POST
def tickets_admin_accommodation_presence_view(request, event, limit_group_id, accommodation_information_id):
    if not event.tickets_event_meta.is_user_allowed_accommodation_access(request.user):
        raise PermissionDenied()

    limit_group = get_object_or_404(LimitGroup, event=event, id=limit_group_id)
    accommodee = get_object_or_404(
        AccommodationInformation,
        limit_groups=limit_group,
        id=accommodation_information_id,
    )

    accommodee_form = initialize_form(AccommodationPresenceForm, request, instance=accommodee)
    State = AccommodationInformation.State

    if accommodee_form.is_valid():
        action = request.POST.get("action", "save")
        accommodee = accommodee_form.save(commit=False)

        if action == "left":
            accommodee.state = State.LEFT
            event_type = "tickets.accommodation.presence.left"
            message = _("Accommodee marked as left.")

        elif action == "arrived":
            accommodee.state = State.ARRIVED
            event_type = "tickets.accommodation.presence.arrived"
            message = _("Accommodee marked as arrived.")

        else:
            event_type = None
            message = _("Accommodation information saved.")

        accommodee.save()

        if event_type:
            emit(
                event_type,
                request=request,
                event=event,
                accommodation_information=accommodee,
                limit_group=limit_group,
                other_fields=dict(room_name=accommodee.room_name),
            )

        messages.success(request, message)

    else:
        messages.error(request, _("Please check the form."))

    return redirect("tickets_admin_accommodation_filtered_view", event.slug, limit_group_id)


@tickets_event_required
@require_http_methods(["GET", "HEAD", "POST"])
def tickets_admin_accommodation_create_view(request, event, limit_group_id):
    if not event.tickets_event_meta.is_user_allowed_accommodation_access(request.user):
        raise PermissionDenied()

    vars = dict(event=event)

    limit_group_id = int(limit_group_id)
    limit_group = get_object_or_404(LimitGroup, id=limit_group_id, event=event)

    form = initialize_form(AccommodationInformationAdminForm, request)

    if request.method == "POST":
        if form.is_valid():
            info = form.save(commit=False)
            info.state = AccommodationInformation.State.ARRIVED
            info.save()

            info.limit_groups.set([limit_group])

            emit(
                "tickets.accommodation.presence.arrived",
                request=request,
                event=event,
                accommodation_information=info,
                limit_group=limit_group,
                other_fields=dict(room_name=info.room_name),
            )

            messages.success(request, "Majoittuja lisättiin.")
        else:
            messages.error(request, _("Please check the form."))

        return redirect("tickets_admin_accommodation_filtered_view", event.slug, limit_group_id)

    vars.update(
        form=form,
        limit_group=limit_group,
    )

    return render(request, "tickets_admin_accommodation_create_view.pug", vars)


class KompassiPOSView(POSView):
    def get_valid_codes(self, request):
        # Kompassi uses the MIR state for cancelled orders.
        return super().get_valid_codes(request).exclude(status__in=(MANUAL_INTERVENTION_REQUIRED, BEYOND_LOGIC))


lippukala_pos_view = KompassiPOSView.as_view()


@csrf_exempt
@tickets_event_required
def tickets_admin_pos_view(request, event):
    # XXX kala expects event filter via &event=foo; we specify it via /events/foo
    request.GET = request.GET.copy()
    request.GET["event"] = event.slug

    meta = event.tickets_event_meta
    if not meta:
        messages.error(request, "Tämä tapahtuma ei käytä Kompassia lipunmyyntiin.")
        return redirect("core_event_view", event.slug)

    if not meta.is_user_allowed_pos_access(request.user):
        return login_redirect(request)

    return lippukala_pos_view(request)


def tickets_admin_menu_items(request, event):
    stats_url = url("tickets_admin_stats_view", event.slug)
    stats_active = request.path == stats_url
    stats_text = "Myyntitilanne"

    orders_url = url("tickets_admin_orders_view", event.slug)
    orders_active = request.path.startswith(orders_url)
    orders_text = "Tilaukset"

    accommodation_url = url("tickets_admin_accommodation_view", event.slug)
    accommodation_active = request.path.startswith(accommodation_url)
    accommodation_text = "Majoituslistat"

    tools_url = url("tickets_admin_tools_view", event.slug)
    tools_active = request.path.startswith(tools_url)
    tools_text = "Työkalut"

    reports_url = url("tickets_admin_reports_view", event.slug)
    reports_active = request.path == reports_url
    reports_text = _("Reports")

    pos_url = url("tickets_admin_pos_view", event.slug)
    pos_active = False
    pos_text = "Lipuntarkastus"

    return [
        (stats_active, stats_url, stats_text),
        (orders_active, orders_url, orders_text),
        (accommodation_active, accommodation_url, accommodation_text),
        (tools_active, tools_url, tools_text),
        (pos_active, pos_url, pos_text),
        (reports_active, reports_url, reports_text),
    ]


@tickets_admin_required
def tickets_admin_export_view(request, vars, event, format="xlsx"):
    ops = OrderProduct.objects.filter(
        order__event=event,
        # Order is confirmed
        order__confirm_time__isnull=False,
        # Order is paid
        order__payment_date__isnull=False,
        # Order is not cancelled
        order__cancellation_time__isnull=True,
        count__gte=1,
    ).order_by("order__payment_date", "id")

    timestamp = now().strftime("%Y%m%d%H%M%S")

    return csv_response(
        event,
        OrderProduct,
        ops,
        dialect=next(fmt for fmt in EXPORT_FORMATS if fmt.extension == format).csv_dialect,
        filename=f"{event.slug}_ticketsales_{timestamp}.{format}",
    )
