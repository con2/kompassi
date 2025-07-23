import datetime
from collections import defaultdict

from django.contrib import messages
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_safe
from lippukala.consts import BEYOND_LOGIC, MANUAL_INTERVENTION_REQUIRED
from lippukala.views import POSView

from kompassi.core.utils import initialize_form, login_redirect, url
from kompassi.event_log_v2.utils.emit import emit

from ..forms import (
    AdminOrderForm,
    CustomerForm,
    OrderProductForm,
    SearchForm,
)
from ..helpers import perform_search, tickets_admin_required, tickets_event_required
from ..models import (
    Order,
)
from ..models.LEGACY_TICKETSV1_consts import UNPAID_CANCEL_HOURS
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
    emit("core.person.viewed", request=request)

    return render(request, "tickets_admin_order_view.pug", vars)


@tickets_admin_required
@require_safe
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
        (tools_active, tools_url, tools_text),
        (pos_active, pos_url, pos_text),
        (reports_active, reports_url, reports_text),
    ]
