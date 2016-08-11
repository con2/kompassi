# encoding: utf-8

from labour.models import PersonnelClass


def get_priority(pair):
    personnel_class, job_title = pair
    return personnel_class.priority


def default_badge_factory(event, person):
    """
    Specifies badge options, such as badge template and job title, given an event and a person.

    Returns a dictionary that can be fed into the constructor of badges.models:Badge.

    If the key `personnel_class` in that dictionary is None, that person should not have a badge.
    """

    personnel_classes = []

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

        # Insertion order matters (most privileged first). list.sort is guaranteed to be stable.
        personnel_classes.extend(
            (programme_role.role.personnel_class, programme_role.role.public_title)
            for programme_role in ProgrammeRole.objects.filter(
                person=person,
                programme__category__event=event,
                programme__state__in=['accepted', 'published']
            ).order_by('role__priority')
        )

    if personnel_classes:
        personnel_classes.sort(key=get_priority)
        personnel_class, job_title = personnel_classes[0]
    else:
        personnel_class = None
        job_title = u'THIS BADGE SHOULD NOT PRINT' # This should never get printed.

    meta = event.badges_event_meta

    return dict(
        first_name=person.first_name,
        is_first_name_visible=meta.real_name_must_be_visible or person.is_first_name_visible,
        surname=person.surname,
        is_surname_visible=meta.real_name_must_be_visible or person.is_surname_visible,
        nick=person.nick,
        is_nick_visible=person.is_nick_visible,
        personnel_class=personnel_class,
        job_title=job_title,
    )
