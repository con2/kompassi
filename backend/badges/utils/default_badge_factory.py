from typing import Any

from core.models.event import Event
from core.models.person import Person


def get_priority(pair):
    personnel_class, job_title = pair
    return personnel_class.priority


def default_badge_factory(event: Event, person: Person) -> dict[str, Any]:
    """
    Specifies badge options, such as badge template and job title, given an event and a person.

    Returns a dictionary that can be fed into the constructor of badges.models:Badge.

    If the key `personnel_class` in that dictionary is None, that person should not have a badge.
    """
    from labour.models.personnel_class import PersonnelClass

    personnel_classes: list[tuple[PersonnelClass, str]] = []

    if event.labour_event_meta is not None:
        from labour.models import Signup

        try:
            signup = Signup.objects.get(event=event, person=person, is_active=True)
        except Signup.DoesNotExist:
            pass
        else:
            job_title = signup.some_job_title
            personnel_classes.extend((pc, job_title) for pc in signup.personnel_classes.all())

    if event.programme_event_meta is not None:
        from programme.models import ProgrammeRole
        from programme.models.programme import PROGRAMME_STATES_LIVE

        # Insertion order matters (most privileged first). list.sort is guaranteed to be stable.
        personnel_classes.extend(
            (programme_role.role.personnel_class, programme_role.role.public_title)
            for programme_role in ProgrammeRole.objects.filter(
                person=person,
                programme__category__event=event,
                programme__state__in=PROGRAMME_STATES_LIVE,
            )
            .order_by("role__priority")
            .select_related("role")
        )

    # Implement Survey to Badge (STB).
    # See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn
    if event.forms_event_meta is not None:
        from ..models.survey_to_badge import SurveyToBadgeMapping

        for survey_mapping in (
            SurveyToBadgeMapping.objects.filter(
                survey__event=event,
            )
            .select_related("personnel_class")
            .order_by("priority")
        ):
            for _response, personnel_class, job_title in survey_mapping.match(person):
                personnel_classes.append((personnel_class, job_title))

    if personnel_classes:
        personnel_classes.sort(key=get_priority)
        personnel_class, job_title = personnel_classes[0]
    else:
        personnel_class = None
        job_title = "THIS BADGE SHOULD NOT PRINT"  # This should never get printed.

    meta = event.badges_event_meta

    return dict(
        first_name=person.first_name,
        is_first_name_visible=meta.real_name_must_be_visible or "firstname" in person.badge_name_display_style,
        surname=person.surname,
        is_surname_visible=meta.real_name_must_be_visible or "surname" in person.badge_name_display_style,
        nick=person.nick,
        # NOTE: Explicit cast required, or the empty string '' in person.nick will cause this predicate to return ''
        is_nick_visible=bool(person.nick) and "nick" in person.badge_name_display_style,
        personnel_class=personnel_class,
        job_title=job_title,
    )
