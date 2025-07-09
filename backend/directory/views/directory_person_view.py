from __future__ import annotations

from dataclasses import dataclass

from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from access.cbac import default_cbac_required
from core.models.event import Event
from core.models.organization import Organization
from core.models.person import Person
from enrollment.models import Enrollment
from labour.models import ArchivedSignup, Signup
from membership.models import Membership
from programme.models import ProgrammeRole


@dataclass
class Involvement:
    event: Event
    signup: Signup | ArchivedSignup | None
    enrollment: Enrollment | None
    programme_roles: QuerySet[ProgrammeRole]
    current_user_is_labour_admin: bool
    current_user_is_programme_admin: bool
    current_user_is_enrollment_admin: bool

    @classmethod
    def get(cls, request: HttpRequest, event: Event, person: Person):
        signup = ArchivedSignup.objects.filter(person=person, event=event).first()
        if not signup:
            signup = Signup.objects.filter(person=person, event=event).first()

        return Involvement(
            event=event,
            signup=signup,
            enrollment=Enrollment.objects.filter(person=person, event=event).first(),
            programme_roles=ProgrammeRole.objects.filter(person=person, programme__category__event=event),
            current_user_is_labour_admin=(
                event.labour_event_meta and event.labour_event_meta.is_user_admin(request.user)
            ),
            current_user_is_programme_admin=(
                event.programme_event_meta and event.programme_event_meta.is_user_admin(request.user)
            ),
            current_user_is_enrollment_admin=(
                event.enrollment_event_meta and event.enrollment_event_meta.is_user_admin(request.user)
            ),
        )


@default_cbac_required
@require_http_methods(["GET", "HEAD", "POST"])
def directory_person_view(request: HttpRequest, organization_slug: str, person_id: str):
    organization = get_object_or_404(Organization, slug=organization_slug)
    person = get_object_or_404(organization.people, id=int(person_id))
    membership = Membership.objects.filter(organization=organization, person=person).first()

    t = now()
    past_events = person.get_events(end_time__lt=t, organization=organization).order_by("-start_time")
    current_events = person.get_events(start_time__lte=t, end_time__gt=t, organization=organization)
    future_events = person.get_events(start_time__gte=t, organization=organization)

    involvement_in_past_events = [Involvement.get(request, event, person) for event in past_events]
    involvement_in_current_events = [Involvement.get(request, event, person) for event in current_events]
    involvement_in_future_events = [Involvement.get(request, event, person) for event in future_events]

    vars = dict(
        organization=organization,
        person=person,
        membership=membership,
        involvement_in_past_events=involvement_in_past_events,
        involvement_in_current_events=involvement_in_current_events,
        involvement_in_future_events=involvement_in_future_events,
    )

    person.log_view(request)

    return render(request, "directory_person_view.pug", vars)
