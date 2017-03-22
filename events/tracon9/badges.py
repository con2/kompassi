# encoding: utf-8



from labour.models import Signup
from badges.models import Template
from programme.models import Programme


def badge_factory(event, person):
    # Labour badges
    try:
        signup = Signup.objects.get(event=event, person=person)
    except Signup.DoesNotExist:
        pass
    else:
        # Priority badges in order
        template_names = ['Conitea', 'Ylivänkäri']

        for template_name in template_names:
            if signup.job_categories_accepted.filter(name=template_name).exists():
                return dict(
                    template=Template.objects.get(event=event, name=template_name),
                    job_title=signup.job_title or template_name,
                )

        # Normal worker badge
        return dict(
            template=Template.objects.get(event=event, name='Työvoima'),
            job_title=signup.some_job_title,
        )

    # Programme badges
    if Programme.objects.filter(category__event=event, organizers=person).exists():
        return dict(
            template=Template.objects.get(event=event, name='Ohjelmanjärjestäjä'),
            job_title='Ohjelmanjärjestäjä'
        )

    # Neither labour nor programme
    raise NotImplemented()
