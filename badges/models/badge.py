# encoding: utf-8

from django.db import models
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin
from core.utils import time_bool_property


class Badge(models.Model, CsvExportMixin):
    person = models.ForeignKey('core.Person',
        null=True,
        blank=True,
        verbose_name=_(u'Person'),
    )

    personnel_class = models.ForeignKey('labour.PersonnelClass',
        verbose_name=_(u'Personnel class'),
    )

    printed_separately_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_(u'Printed separately at'),
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_(u'Revoked at'),
    )

    first_name = models.CharField(
        max_length=1023,
        verbose_name=_(u'First name'),
    )
    is_first_name_visible = models.BooleanField(
        default=True,
        verbose_name=_(u'Is first_name visible'),
    )

    surname = models.CharField(
        max_length=1023,
        verbose_name=_(u'Surname'),
    )
    is_surname_visible = models.BooleanField(
        default=True,
        verbose_name=_(u'Is surname visible'),
    )

    nick = models.CharField(
        blank=True,
        max_length=1023,
        help_text=_(u'Nick name'),
    )
    is_nick_visible = models.BooleanField(
        default=True,
        verbose_name=_(u'Is nick visible'),
    )

    job_title = models.CharField(max_length=63,
        blank=True,
        default=u'',
        verbose_name=_(u'Job title'))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u'Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_(u'Updated at'),
    )

    batch = models.ForeignKey('badges.Batch',
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_(u'Printing batch'),
    )

    is_revoked = time_bool_property('revoked_at')
    is_printed = time_bool_property('printed_at')
    is_printed_separately = time_bool_property('printed_separately_at')

    @property
    def printed_at(self):
        if self.batch:
            return self.batch.printed_at
        else:
            return self.printed_separately_at

    @property
    def formatted_printed_at(self):
        # XXX not really "formatted"
        return self.printed_at if self.printed_at is not None else u''

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Person
        from labour.models import PersonnelClass

        person, unused = Person.get_or_create_dummy()
        personnel_class, unused = PersonnelClass.get_or_create_dummy()

        return cls.objects.get_or_create(
            person=person,
            personnel_class=personnel_class,
        )

    @classmethod
    def get_or_create(cls, event, person):
        # FIXME If someone first does programme and then labour, they should still get labour badge.
        # Factory should be invoked anyway, and badge "upgraded" (revoke old, create new).
        # https://jira.tracon.fi/browse/CONDB-422

        assert person is not None

        try:
            return cls.objects.get(
                personnel_class__event=event,
                person=person,
                revoked_at__isnull=True,
            ), False
        except cls.DoesNotExist:
            from badges.utils import default_badge_factory

            badge_opts = default_badge_factory(event=event, person=person)
            badge_opts = dict(badge_opts, person=person)

            badge = cls(**badge_opts)
            badge.save()

            return badge, True

    @classmethod
    def get_csv_fields(cls, event):
        from labour.models import PersonnelClass

        meta = event.badges_event_meta
        if meta.badge_layout == 'trad':
            # Chief Technology Officer
            # Santtu Pajukanta
            # Japsu
            return [
                (cls, 'personnel_class_name'),
                (BadgePrivacyProxy, 'surname'),
                (BadgePrivacyProxy, 'first_name'),
                (BadgePrivacyProxy, 'nick'),
                (cls, 'job_title'),
            ]
        elif meta.badge_layout == 'nick':
            # JAPSU
            # Santtu Pajukanta
            # Chief Technology Officer
            # -OR-
            # SANTTU
            # Pajukanta
            # Chief Technology Officer
            return [
                (cls, 'personnel_class_name')
                (BadgePrivacyProxy, 'nick_or_first_name'),
                (BadgePrivacyProxy, 'surname_or_full_name'),
                (cls, 'job_title'),
            ]
        else:
            raise NotImplementedError(meta.badge_layout)

    def get_csv_related(self):
        from core.models import Person

        return {
            BadgePrivacyProxy: BadgePrivacyProxy(self),
        }

    def get_name_fields(self):
        return [
            (self.person.surname.strip(), self.is_surname_visible),
            (self.person.first_name.strip(), self.is_first_name_visible),
            (self.person.nick.strip(), self.is_nick_visible),
        ]

    @property
    def personnel_class_name(self):
        return self.personnel_class.name if self.personnel_class else u''

    @property
    def event(self):
        return self.personnel_class.event

    @property
    def meta(self):
        return self.event.badges_event_meta

    @property
    def event_name(self):
        return self.personnel_class.event.name if self.personnel_class else u''

    def to_html_print(self):
        def format_name_field(value, is_visible):
            if is_visible:
                return u"<strong>{value}</strong>".format(value=escape(value))
            else:
                return escape(value)

        vars = dict(
            surname=format_name_field(self.person.surname.strip(), self.is_surname_visible),
            first_name=format_name_field(self.person.first_name.strip(), self.is_first_name_visible),
            nick=format_name_field(self.person.nick.strip(), self.is_nick_visible),
        )

        if self.person.nick:
            return u"{surname}, {first_name}, {nick}".format(**vars)
        else:
            return u"{surname}, {first_name}".format(**vars)

    def revoke(self, user=None):
        assert not self.is_revoked
        self.is_revoked = True
        self.revoked_by = user
        self.save()
        return self

    def unrevoke(self):
        assert self.is_revoked
        self.is_revoked = False
        self.revoked_by = None
        self.save()
        return self

    def admin_get_full_name(self):
        if self.nick:
            return u'{self.first_name} "{self.nick}" {self.surname}'.format(self=self)
        else:
            return u'{self.first_name} {self.surname}'.format(self=self)
    admin_get_full_name.short_description = _(u'Name')
    admin_get_full_name.admin_order_field = ('surname', 'first_name', 'nick')

    def __unicode__(self):
        return u"{person_name} ({personnel_class_name}, {event_name})".format(
            person_name=self.admin_get_full_name(),
            personnel_class_name=self.personnel_class_name,
            event_name=self.event_name,
        )
