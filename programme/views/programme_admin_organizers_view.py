# encoding: utf-8

from collections import defaultdict

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_safe

from core.models import Person
from core.sort_and_filter import Filter, Sorter
from core.utils import initialize_form, groupby_strict
from labour.models import PersonnelClass

from ..helpers import programme_admin_required
from ..models import Programme, ProgrammeRole


@programme_admin_required
@require_safe
def programme_admin_organizers_view(request, vars, event):
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
    personnel_class_filters = Filter(request, 'personnel_class').add_objects('role__personnel_class__slug', personnel_classes)
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
        num_organizers=len(organizers),
        num_total_organizers=Person.objects.filter(programme__category__event=event).distinct().count(),
        organizers=organizers,
        personnel_class_filters=personnel_class_filters,
    )

    return render(request, 'programme_admin_organizers_view.jade', vars)
