from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.http import require_safe

from kompassi.core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat, csv_response
from kompassi.core.models import Person
from kompassi.core.sort_and_filter import Filter
from kompassi.core.utils import groupby_strict
from kompassi.event_log_v2.utils.emit import emit
from kompassi.labour.models import PersonnelClass

from ..helpers import programme_admin_required
from ..models import AlternativeProgrammeForm, ProgrammeRole, Role

EXPORT_FORMATS = [
    *EXPORT_FORMATS,
    ExportFormat("Sähköpostiosoitteet", "txt", "txt"),
]


@programme_admin_required
@require_safe
def admin_organizers_view(request, vars, event, format="screen"):
    programme_roles = (
        ProgrammeRole.objects.filter(programme__category__event=event)
        .select_related("person")
        .select_related("programme")
        .select_related("role")
        .order_by("person__surname", "person__first_name", "programme__title")
    )

    personnel_classes = PersonnelClass.objects.filter(
        event=event,
        role__personnel_class__event=event,
    )
    personnel_class_filters = Filter(request, "personnel_class")
    personnel_class_filters.add_objects("role__personnel_class__slug", personnel_classes)
    programme_roles = personnel_class_filters.filter_queryset(programme_roles)

    roles = Role.objects.filter(personnel_class__event=event)
    role_filters = Filter(request, "role")
    role_filters.add_objects("role__slug", roles)
    programme_roles = role_filters.filter_queryset(programme_roles)

    forms = AlternativeProgrammeForm.objects.filter(event=event)
    form_filters = Filter(request, "form")
    form_filters.add_objects("programme__form_used__slug", forms)
    programme_roles = form_filters.filter_queryset(programme_roles)

    active_filters = Filter(request, "active").add_booleans("is_active")
    programme_roles = active_filters.filter_queryset(programme_roles)

    organizers = []
    prs_by_organizer = groupby_strict(programme_roles, lambda pr: pr.person)
    for organizer, prs in prs_by_organizer:
        organizer.current_event_programme_roles = prs
        organizers.append(organizer)

    vars.update(
        active_filters=active_filters,
        export_formats=EXPORT_FORMATS,
        form_filters=form_filters,
        num_organizers=len(organizers),
        num_total_organizers=Person.objects.filter(programme__category__event=event).distinct().count(),
        organizers=organizers,
        personnel_class_filters=personnel_class_filters,
        role_filters=role_filters,
    )

    if format == "screen":
        return render(request, "programme_admin_organizers_view.pug", vars)
    elif format == "txt":
        emails = "\n".join(programme_roles.order_by("person__email").values_list("person__email", flat=True).distinct())
        emit("core.person.exported", request=request)
        return HttpResponse(emails, content_type="text/plain")
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programme_organizers_{timestamp}.{format}".format(
            event=event,
            timestamp=now().strftime("%Y%m%d%H%M%S"),
            format=format,
        )

        emit("core.person.exported", request=request)

        return csv_response(
            event,
            ProgrammeRole,
            programme_roles,
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
            m2m_mode="separate_columns",
        )
    else:
        raise NotImplementedError(format)
