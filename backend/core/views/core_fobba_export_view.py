from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.decorators.http import require_safe
from paikkala.models import Ticket

from badges.models import Badge
from core.excel_export import XlsxWriter
from core.models import Event
from event_log_v2.utils.emit import emit
from tickets.models import Order


@require_safe
@user_passes_test(lambda user: user.is_superuser)
def core_fobba_export_view(request, event_slug, format="xlsx"):
    event = Event.objects.get(slug=event_slug)
    timestamp = now().strftime("%Y%m%d%H%M%S")
    filename = f"{event.slug}_police_export_{timestamp}.xlsx"

    emit(
        "core.person.exported",
        request=request,
        other_fields=dict(filename=filename),
    )

    response = HttpResponse()
    response["content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = XlsxWriter(response)
    writer.writerow(
        [
            "surname",
            "first_name",
            "email",
            "phone_number",
            "role",
            "role_extra",
        ]
    )

    seen = set()

    for badge in Badge.objects.filter(personnel_class__event=event, revoked_at__isnull=True):
        id_fields = (
            badge.surname,
            badge.first_name,
            badge.person.email if badge.person else "",
            badge.person.normalized_phone_number if badge.person else "",
        )

        if id_fields in seen:
            continue

        seen.add(id_fields)
        writer.writerow(
            [
                *id_fields,
                badge.personnel_class_name,
                badge.job_title,
            ]
        )

    for order in Order.objects.filter(
        event=event,
        confirm_time__isnull=False,
        payment_date__isnull=False,
        cancellation_time__isnull=True,
    ):
        customer = order.customer
        if not customer:
            raise AssertionError("customer missing")

        id_fields = (
            customer.last_name,
            customer.first_name,
            customer.email,
            customer.normalized_phone_number,
        )

        if id_fields in seen:
            continue

        seen.add(id_fields)
        writer.writerow(
            [
                *id_fields,
                "Lipun ostaja",
                order.formatted_order_products,
            ]
        )

    for ticket in Ticket.objects.filter(program__kompassi_programme__category__event=event):
        person = ticket.user.person  # type: ignore

        id_fields = (
            person.surname,
            person.first_name,
            person.email,
            person.normalized_phone_number,
        )

        if id_fields in seen:
            continue

        seen.add(id_fields)
        writer.writerow(
            [
                *id_fields,
                "Paikkalipun varaaja",
                "",
            ]
        )

    writer.close()
    return response
