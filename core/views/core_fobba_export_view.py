from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.http import require_safe
from django.http import HttpResponse

from badges.models import Badge
from core.models import Event
from core.excel_export import XlsxWriter
from tickets.models import Order
from event_log.utils import emit


@require_safe
@user_passes_test(lambda user: user.is_superuser)
def core_fobba_export_view(request, event_slug, format="xlsx"):
    event = Event.objects.get(slug=event_slug)
    timestamp = now().strftime("%Y%m%d%H%M%S")
    filename = f"{event.slug}_police_export_{timestamp}.xlsx"

    emit(
        "core.person.exported",
        request=request,
        event=event,
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

    for badge in Badge.objects.filter(personnel_class__event=event):
        writer.writerow(
            [
                badge.surname,
                badge.first_name,
                badge.person.email if badge.person else "",
                badge.person.normalized_phone_number if badge.person else "",
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
        assert customer

        writer.writerow(
            [
                customer.last_name,
                customer.first_name,
                customer.email,
                customer.normalized_phone_number,
                "Lipun ostaja",
                order.formatted_order_products,
            ]
        )

    writer.close()
    return response
