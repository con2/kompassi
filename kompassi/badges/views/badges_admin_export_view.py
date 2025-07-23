from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_safe

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, csv_response

from ..helpers import badges_admin_required
from ..models import Badge, Batch


@badges_admin_required
@require_safe
def badges_admin_export_view(request, vars, event, batch_id, format="csv"):
    if format not in CSV_EXPORT_FORMATS:
        raise NotImplementedError(format)

    batch = get_object_or_404(Batch, pk=int(batch_id), event=event)
    badges = batch.badges.all()

    filename = f"{event.slug}-badges-batch{batch.pk}.{format}"

    return csv_response(event, Badge, badges, filename=filename, dialect=CSV_EXPORT_FORMATS[format])
