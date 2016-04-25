# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify, url
from core.models import OneTimeCode, OneTimeCodeLite


class Role(models.Model):
    personnel_class = models.ForeignKey('labour.PersonnelClass',
        verbose_name=_(u'Personnel class'),
        help_text=_(u'The personnel class for the programme hosts that have this role.'),
    )

    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(
        default=True,
        verbose_name=_(u'Public'),
        help_text=_(u'Only hosts who are assigned public roles will be shown publicly in the programme schedule.'),
    )

    priority = models.IntegerField(
        default=0,
        verbose_name=_(u'Priority'),
        help_text=_(u'Some events have speaker roles that convey different privileges within the same personnel class. This priority field will put the speakers in their place.'),
    )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')
        ordering = ('personnel_class__event', 'personnel_class__priority', 'priority')

    @classmethod
    def get_or_create_dummy(cls, personnel_class=None, priority=0, title=u'Overbaron'):
        from labour.models import PersonnelClass

        if personnel_class is None:
            personnel_class, unused = PersonnelClass.get_or_create_dummy(
                app_label='programme',
                name='Entertainer',
                priority=40,
            )

        return cls.objects.get_or_create(
            personnel_class=personnel_class,
            title=title,
            defaults=dict(
                priority=priority,
                require_contact_info=False,
            )
        )

    def admin_get_event(self):
        return self.personnel_class.event if self.personnel_class else None
    admin_get_event.short_description = _(u'Event')
    admin_get_event.admin_order_field = 'personnel_class__event'