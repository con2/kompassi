from django.http import HttpResponse
from django.shortcuts import render

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat

from ..helpers import intra_organizer_required
from ..models import Team

EXPORT_FORMATS = [
    *EXPORT_FORMATS,
    ExportFormat("vCard", "vcf", "vcf"),
]

HTML_TEMPLATES = dict(
    screen="intra_organizer_view.pug",
)


@intra_organizer_required
def intra_organizer_view(request, vars, event, format="screen"):
    meta = event.intra_event_meta
    is_admin = meta.is_user_admin(request.user)

    teams_criteria = dict(event=event)
    if not is_admin:
        teams_criteria.update(is_public=True)
    teams = Team.objects.filter(**teams_criteria).prefetch_related("members")

    vars.update(
        num_total_organizers=meta.organizer_group.user_set.count(),
        num_unassigned_organizers=len(meta.unassigned_organizers),
        teams=teams,
        unassigned_organizers=meta.unassigned_organizers,
    )

    if format in HTML_TEMPLATES:
        template = HTML_TEMPLATES[format]
        return render(request, template, vars)
    elif format == "vcf":
        return HttpResponse(
            "".join(user.person.as_vcard(event=event) for user in meta.organizer_group.user_set.all()),
            content_type="text/vcard",
        )
    elif format in CSV_EXPORT_FORMATS:
        raise NotImplementedError(format)
    else:
        raise NotImplementedError(format)
