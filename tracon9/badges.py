from labour.models import Signup
from badges.models import Template


def badge_factory(event, person):
    # Labour badges
    try:
        signup = Signup.objects.get(event=event, person=person)
    except Signup.DoesNotExist:
        pass
    else:
        # Priority badges in order
        template_names = [u'Conitea', u'Ylivänkäri']

        for template_name in template_names:
            if signup.job_categories_accepted.filter(name=template_name).exists():
                return dict(
                    template=Template.objects.get(event=event, name=template_name),
                    job_title=signup.job_title or template_name,
                )

        # Normal worker badge
        return dict(
            template=Template.objects.get(event=event, name=u'Työvoima'),
            job_title=signup.job_title or u'Työvoima',
        )

    # Programme badges
    if Programme.objects.filter(category__event=event, organizers=person).exists():
        return dict(
            template=Template.objects.get(event=event, name=u'Ohjelma'),
            job_title=u'Ohjelmanjärjestäjä'
        )

    # Neither labour nor programme
    raise NotImplemented()