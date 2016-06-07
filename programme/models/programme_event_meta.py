# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from core.utils import alias_property
from core.models import EventMetaBase, ContactEmailMixin, contact_email_validator


class ProgrammeEventMeta(ContactEmailMixin, EventMetaBase):
    public_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Ohjelmakartan julkaisuaika',
        help_text=u'Ohjelmakartta näkyy kansalle tästä eteenpäin.',
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        validators=[contact_email_validator,],
        verbose_name=u'yhteysosoite',
        help_text=u'Kaikki ohjelmajärjestelmän lähettämät sähköpostiviestit lähetetään tästä '
            u'osoitteesta, ja tämä osoite näytetään ohjelmanjärjestäjälle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.',
    )

    def get_special_programmes(self, include_unpublished=False):
        from .room import Room
        from .programme import Programme

        schedule_rooms = Room.objects.filter(view__event=self.event).only('id')
        criteria = dict(category__event=self.event)
        if not include_unpublished:
            criteria.update(state='published')
        return Programme.objects.filter(**criteria).exclude(room__in=schedule_rooms)

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event

        event, unused = Event.get_or_create_dummy()
        admin_group, = cls.get_or_create_groups(event, ['admins'])

        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                public=True
            )
        )

    @property
    def is_public(self):
        return self.public_from is not None and now() > self.public_from

    public = alias_property('is_public')

    @property
    def signup_extra_model(self):
        if self.event.labour_event_meta is not None:
            return self.event.labour_event_meta.signup_extra_model
        else:
            from labour.models import EmptySignupExtra
            return EmptySignupExtra
