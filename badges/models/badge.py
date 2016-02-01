# encoding: utf-8

from django.conf import settings
from django.db import models, transaction
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin
from core.utils import time_bool_property

from ..proxies.badge.privacy import BadgePrivacyAdapter


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

    revoked_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='badges_revoked',
        verbose_name=_(u'Revoked by'),
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_(u'Revoked at'),
    )

    first_name = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_(u'First name'),
    )
    is_first_name_visible = models.BooleanField(
        default=True,
        verbose_name=_(u'Is first name visible'),
    )

    surname = models.CharField(
        blank=True,
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
        verbose_name=_(u'Nick name'),
        help_text=_(u'If you only have a single piece of information to print on the badge, use this field.'),
    )
    is_nick_visible = models.BooleanField(
        default=True,
        verbose_name=_(u'Is nick visible'),
    )

    job_title = models.CharField(max_length=63,
        blank=True,
        default=u'',
        verbose_name=_(u'Job title'),
        help_text=_(u'Please stay civil with the job title field.'),
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='badges_created',
        verbose_name=_(u'Created by'),
    )
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
        if self.printed_separately_at:
            return self.printed_separately_at
        elif self.batch:
            return self.batch.printed_at
        else:
            return None

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
    def ensure(cls, event, person):
        """
        Makes sure the person has a badge of the correct class and up-to-date information for a given event.
        """

        from badges.utils import default_badge_factory

        assert person is not None

        with transaction.atomic():
            try:
                existing_badge = cls.objects.get(
                    personnel_class__event=event,
                    person=person,
                    revoked_at__isnull=True,
                )
            except cls.DoesNotExist:
                existing_badge = None

            expected_badge_opts = default_badge_factory(event=event, person=person)

            if existing_badge:
                # There is an existing un-revoked badge. Check that its information is correct.
                if any(getattr(existing_badge, key) != value for key, value in expected_badge_opts.iteritems()):
                    existing_badge.revoke()
                else:
                    return existing_badge, False

            if expected_badge_opts.get('personnel_class') is None:
                # They should not have a badge.
                return None, False

            badge_opts = dict(expected_badge_opts, person=person)

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
                (BadgePrivacyAdapter, 'surname'),
                (BadgePrivacyAdapter, 'first_name'),
                (BadgePrivacyAdapter, 'nick'),
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
                (cls, 'personnel_class_name'),
                (BadgePrivacyAdapter, 'nick_or_first_name'),
                (BadgePrivacyAdapter, 'surname_or_full_name'),
                (cls, 'job_title'),
            ]
        else:
            raise NotImplementedError(meta.badge_layout)

    def get_csv_related(self):
        from core.models import Person

        return {
            BadgePrivacyAdapter: BadgePrivacyAdapter(self),
        }

    def get_name_fields(self):
        return [
            (self.surname.strip(), self.is_surname_visible),
            (self.first_name.strip(), self.is_first_name_visible),
            (self.nick.strip(), self.is_nick_visible),
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
            surname=format_name_field(self.surname.strip(), self.is_surname_visible),
            first_name=format_name_field(self.first_name.strip(), self.is_first_name_visible),
            nick=format_name_field(self.nick.strip(), self.is_nick_visible),
        )

        if self.nick:
            return u"{surname}, {first_name}, {nick}".format(**vars)
        else:
            return u"{surname}, {first_name}".format(**vars)

    def revoke(self, user=None):
        """
        Revoke the badge.

        When a badge that is not yet assigned to a batch or printed separately is revoked, it is
        removed altogether.

        When a badge that is already assigned to a batch or printed separately is revoked, it will be
        marked as such but not removed, because it needs to be manually removed from distribution.

        Note that the batch does not need to be marked as printed yet for a badge to stay around revoked,
        because a batch that is already created but not yet printed may have been downloaded as Excel
        already. A Batch should never change after being created.
        """
        assert not self.is_revoked

        if self.is_printed_separately or self.batch:
            self.is_revoked = True
            self.revoked_by = user
            self.save()
            return self
        else:
            self.delete()
            return None

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
