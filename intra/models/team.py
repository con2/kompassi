# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


@python_2_unicode_compatible
class Team(models.Model):
    event = models.ForeignKey('core.Event')
    order = models.IntegerField(
        verbose_name=_('Order'),
        default=0,
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )
    description = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Description'),
        help_text=_('What is the team responsible for?'),
    )
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    group = models.ForeignKey('auth.Group')

    panel_css_class = 'panel-default'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        if self.slug and not self.group_id:
            self.group, = self.event.intra_event_meta.get_or_create_groups(self.event, [self.slug])

        return super(Team, self).save(*args, **kwargs)

    @classmethod
    def get_or_create_dummy(cls):
        from .intra_event_meta import IntraEventMeta

        meta, unused = IntraEventMeta.get_or_create_dummy()
        event = meta.event

        return cls.objects.get_or_create(
            event=event,
            slug='dummyteam',
            defaults=dict(
                name='Dummy team',
            ),
        )

    class Meta:
        ordering = ('event', 'order', 'name')
        unique_together = [('event', 'slug'),]
