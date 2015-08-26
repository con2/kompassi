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
            if signup.job_title:
                job_title = signup.job_title
            elif signup.job_categories_accepted.exists():
                job_title = signup.job_categories_accepted.first().name

            personnel_class = signup.personnel_classes.order_by('priority').first()

    return dict(
        personnel_class=personnel_class,
        job_title=job_title,
    )
