# encoding: utf-8

from collections import defaultdict

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_safe

from core.models import Person
from core.utils import initialize_form, groupby_strict

from ..helpers import programme_admin_required
from ..models import Programme, ProgrammeRole


@programme_admin_required
@require_safe
def programme_admin_organizers_view(request, vars, event):
    # programmes = Programme.objects.filter(category__event=event).prefetch_related('organizers')
    # programmes_by_organizer = defaultdict(list)
    # for programme in programmes:
    #     for organizer in programme.organizers.all():
    #         programmes_by_organizer[organizer].append(programme)

    programme_roles = (
        ProgrammeRole.objects.filter(programme__category__event=event)
            .select_related('person')
            .select_related('programme')
            .select_related('role')
            .order_by('person__surname', 'person__first_name', 'programme__title')
    )

    organizers = []
    prs_by_organizer = groupby_strict(programme_roles, lambda pr: pr.person)
    for organizer, prs in prs_by_organizer:
        organizer.current_event_programme_roles = prs
        organizers.append(organizer)

    vars.update(
        organizers=organizers,
        num_organizers=len(organizers),
        num_total_organizers=Person.objects.filter(programme__category__event=event).distinct().count(),
    )

    return render(request, 'programme_admin_organizers_view.jade', vars)
