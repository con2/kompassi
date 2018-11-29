from collections import namedtuple

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now

from labour.models import Signup
from membership.models import Membership
from programme.models import ProgrammeRole
from enrollment.models import Enrollment

from ..helpers import directory_access_required


Involvement = namedtuple('Involvement', [
    'event',
    'signup',
    'enrollment',
    'programme_roles',
    'current_user_is_labour_admin',
    'current_user_is_programme_admin',
    'current_user_is_enrollment_admin',
])


def get_involvement(request, event, person):
    return Involvement(
        event=event,
        signup=Signup.objects.filter(person=person, event=event).first(),
        enrollment=Enrollment.objects.filter(person=person, event=event).first(),
        programme_roles=ProgrammeRole.objects.filter(person=person, programme__category__event=event),
        current_user_is_labour_admin=(
            event.labour_event_meta and
            event.labour_event_meta.is_user_admin(request.user)
        ),
        current_user_is_programme_admin=(
            event.programme_event_meta and
            event.programme_event_meta.is_user_admin(request.user)
        ),
        current_user_is_enrollment_admin=(
            event.enrollment_event_meta and
            event.enrollment_event_meta.is_user_admin(request.user)
        ),
    )


@directory_access_required
@require_http_methods(['GET', 'HEAD', 'POST'])
def directory_person_view(request, vars, organization, person_id):
    person = get_object_or_404(organization.people, id=int(person_id))
    membership = Membership.objects.filter(organization=organization, person=person).first()

    t = now()
    past_events = person.get_events(end_time__lt=t, organization=organization).order_by('-start_time')
    current_events = person.get_events(start_time__lte=t, end_time__gt=t, organization=organization)
    future_events = person.get_events(start_time__gte=t, organization=organization)

    involvement_in_past_events = [get_involvement(request, event, person) for event in past_events]
    involvement_in_current_events = [get_involvement(request, event, person) for event in current_events]
    involvement_in_future_events = [get_involvement(request, event, person) for event in future_events]

    vars.update(
        person=person,
        membership=membership,
        involvement_in_past_events=involvement_in_past_events,
        involvement_in_current_events=involvement_in_current_events,
        involvement_in_future_events=involvement_in_future_events,
    )

    person.log_view(request, organization=organization)

    return render(request, 'directory_person_view.pug', vars)
