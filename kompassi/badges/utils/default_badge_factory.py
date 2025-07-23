from typing import Any

from kompassi.core.models.event import Event
from kompassi.core.models.person import Person

from ..models.survey_to_badge import SurveyToBadgeMapping


def get_priority(pair):
    personnel_class, job_title = pair
    return personnel_class.priority


def default_badge_factory(event: Event, person: Person) -> dict[str, Any]:
    """
    Specifies badge options, such as badge template and job title, given an event and a person.

    Returns a dictionary that can be fed into the constructor of badges.models:Badge.

    If the key `personnel_class` in that dictionary is None, that person should not have a badge.
    """
    from kompassi.involvement.models.involvement_to_badge import InvolvementToBadgeMapping
    from kompassi.labour.models.personnel_class import PersonnelClass

    personnel_classes: list[tuple[PersonnelClass, str]] = []

    if event.labour_event_meta is not None:
        from kompassi.labour.models import Signup

        try:
            signup = Signup.objects.get(event=event, person=person, is_active=True)
        except Signup.DoesNotExist:
            pass
        else:
            job_title = signup.some_job_title
            personnel_classes.extend((pc, job_title) for pc in signup.personnel_classes.all())

    # Survey to Badge (STB).
    # See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn
    # Serves Surveys V2 in an interim capacity (to be replaced by ITB).
    for survey_mapping in (
        SurveyToBadgeMapping.objects.filter(
            survey__event=event,
        )
        .select_related("personnel_class")
        .order_by("priority")
    ):
        for _response, personnel_class, job_title in survey_mapping.match(person):
            personnel_classes.append((personnel_class, job_title))

    # Involvement to Badge (ITB)
    # Serves Program V2 etc.
    for involvement_mapping in (
        InvolvementToBadgeMapping.objects.filter(
            universe__scope__event=event,
        )
        .select_related("personnel_class")
        .order_by("priority")
    ):
        for _involvement, personnel_class, job_title in involvement_mapping.match(person):
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
