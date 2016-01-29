# encoding: utf-8

from labour.models import PersonnelClass


def default_badge_factory(event, person):
    """
    Specifies badge options, such as badge template and job title, given an event and a person.

    Returns a dictionary that can be fed into the constructor of badges.models:Badge.
    """

    job_title = u''

    if event.labour_event_meta is not None:
        from labour.models import Signup

        try:
            signup = Signup.objects.get(event=event, person=person)
        except Signup.DoesNotExist:
            # XXX blatantly assuming it's a programme person
            job_title = u'Ohjelmanjärjestäjä'
            personnel_class = PersonnelClass.objects.get(event=event, slug='ohjelma')
        else:
            job_title = signup.some_job_title
            personnel_class = signup.personnel_classes.order_by('priority').first()

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
