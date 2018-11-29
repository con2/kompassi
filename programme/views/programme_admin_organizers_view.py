from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.views.decorators.http import require_safe

from core.csv_export import CSV_EXPORT_FORMATS, EXPORT_FORMATS, ExportFormat, csv_response
from core.models import Person
from core.sort_and_filter import Filter
from core.utils import groupby_strict
from event_log.utils import emit
from labour.models import PersonnelClass

from ..helpers import programme_admin_required
from ..models import ProgrammeRole


EXPORT_FORMATS = EXPORT_FORMATS + [
    ExportFormat('Sähköpostiosoitteet', 'txt', 'txt'),
]


@programme_admin_required
@require_safe
def programme_admin_organizers_view(request, vars, event, format='screen'):
    programme_roles = (
        ProgrammeRole.objects.filter(programme__category__event=event)
        .select_related('person')
        .select_related('programme')
        .select_related('role')
        .order_by('person__surname', 'person__first_name', 'programme__title')
    )

    personnel_classes = PersonnelClass.objects.filter(
        event=event,
        role__personnel_class__event=event,
    )
    personnel_class_filters = Filter(request, 'personnel_class')
    personnel_class_filters.add_objects('role__personnel_class__slug', personnel_classes)
    programme_roles = personnel_class_filters.filter_queryset(programme_roles)

    active_filters = Filter(request, 'active').add_booleans('is_active')
    programme_roles = active_filters.filter_queryset(programme_roles)

    organizers = []
    prs_by_organizer = groupby_strict(programme_roles, lambda pr: pr.person)
    for organizer, prs in prs_by_organizer:
        organizer.current_event_programme_roles = prs
        organizers.append(organizer)

    vars.update(
        active_filters=active_filters,
        export_formats=EXPORT_FORMATS,
        num_organizers=len(organizers),
        num_total_organizers=Person.objects.filter(programme__category__event=event).distinct().count(),
        organizers=organizers,
        personnel_class_filters=personnel_class_filters,
    )

    if format == 'screen':
        return render(request, 'programme_admin_organizers_view.pug', vars)
    elif format == 'txt':
        emails = '\n'.join(programme_roles.order_by('person__email').values_list('person__email', flat=True).distinct())
        emit('core.person.exported', request=request, event=event)
        return HttpResponse(emails, content_type='text/plain')
    elif format in CSV_EXPORT_FORMATS:
        filename = "{event.slug}_programme_organizers_{timestamp}.{format}".format(
            event=event,
            timestamp=now().strftime('%Y%m%d%H%M%S'),
            format=format,
        )

        emit('core.person.exported', request=request, event=event)

        return csv_response(event, ProgrammeRole, programme_roles,
            dialect=CSV_EXPORT_FORMATS[format],
            filename=filename,
            m2m_mode='separate_columns',
        )
    else:
        raise NotImplementedError(format)
