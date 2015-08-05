from labour.models import PersonnelClass


def default_badge_factory(event, person):
    """
    Specifies badge options, such as badge template and job title, given an event and a person.

    Returns a dictionary that can be fed into the constructor of badges.models:Badge.
    """

    if event.labour_event_meta is not None:
        from labour.models import Signup

        try:
            signup = Signup.objects.get(event=event, person=person)
        except Signup.DoesNotExist:
            job_title = u''
        else:
            job_title = signup.job_title or u''
    else:
        job_title = u''

    return dict(
        personnel_class=PersonnelClass.objects.get(event=event),
        job_title=u'',
    )
