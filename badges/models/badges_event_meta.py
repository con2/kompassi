# encoding: utf-8


from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import EventMetaBase

from .count_badges_mixin import CountBadgesMixin


class BadgesEventMeta(EventMetaBase, CountBadgesMixin):
    badge_layout = models.CharField(
        max_length=4,
        default='trad',
        choices=(('trad', _(u'Traditional')), ('nick', _(u'Emphasize nick name'))),
        verbose_name=u'Badgen asettelu',
        help_text=_(
            u'This controls how fields are grouped in the badge. Traditional: job title, firstname surname, '
            u'nick. Emphasize nick name: first name or nick, surname or full name, job title.'
        ),
    )

    real_name_must_be_visible = models.BooleanField(
        default=False,
        verbose_name=_(u'Require real name to be visible'),
        help_text=_(
            u'In most events, it is up to the person carrying the badge to decide whether or not '
            u'their real name is displayed in their badge. Some choose to go by their first name or nick '
            u'name only. Some events have, however, decided to restrict this and require the first name and '
            u'surname to be visible in all badges. If this option is selected, only the name display styles '
            u'<em>Firstname Surname</em> and <em>Firstname "Nick" Surname</em> are effectively allowed.'
        )
    )

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        group, = cls.get_or_create_groups(event, ['admins'])
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    # for CountBadgesMixin
    @property
    def badge_set(self):
        return Badge.objects.filter(personnel_class__event=self.event)