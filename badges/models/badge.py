import logging

from django.conf import settings
from django.db import models, transaction
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from core.csv_export import CsvExportMixin
from core.utils import time_bool_property

from ..proxies.badge.privacy import BadgePrivacyAdapter


logger = logging.getLogger('kompassi')


class Badge(models.Model, CsvExportMixin):
    person = models.ForeignKey('core.Person', on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('Person'),
        related_name='badges',
    )

    personnel_class = models.ForeignKey('labour.PersonnelClass', on_delete=models.CASCADE,
        verbose_name=_('Personnel class'),
        related_name='badges',
    )

    printed_separately_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Printed separately at'),
    )

    revoked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='badges_revoked',
        verbose_name=_('Revoked by'),
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Revoked at'),
    )

    arrived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Arrived at'),
    )

    first_name = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_('First name'),
    )
    is_first_name_visible = models.BooleanField(
        default=True,
        verbose_name=_('Is first name visible'),
    )

    surname = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_('Surname'),
    )
    is_surname_visible = models.BooleanField(
        default=True,
        verbose_name=_('Is surname visible'),
    )

    nick = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_('Nick name'),
        help_text=_('If you only have a single piece of information to print on the badge, use this field.'),
    )
    is_nick_visible = models.BooleanField(
        default=True,
        verbose_name=_('Is nick visible'),
    )

    job_title = models.CharField(max_length=63,
        blank=True,
        default='',
        verbose_name=_('Job title'),
        help_text=_('Please stay civil with the job title field.'),
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='badges_created',
        verbose_name=_('Created by'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    batch = models.ForeignKey('badges.Batch',
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_('Printing batch'),
        on_delete=models.SET_NULL,
        related_name='badges',
    )

    is_revoked = time_bool_property('revoked_at')
    is_printed = time_bool_property('printed_at')
    is_printed_separately = time_bool_property('printed_separately_at')
    is_arrived = time_bool_property('arrived_at')

    notes = models.TextField(
        default='',
        blank=True,
        verbose_name=_('Internal notes'),
        help_text=_('Internal notes are only visible to the event organizer. However, if the person in question requests a transcript of records, this field is also disclosed.'),
    )

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
        return self.printed_at if self.printed_at is not None else ''

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
            new_badge_opts = dict(expected_badge_opts)

            if event.badges_event_meta.is_using_fuzzy_reissuance_hack:
                # The fuzzy reissuance hack is documented at
                # badges.models.badges_event_meta:Badge.is_using_fuzzy_reissuance_hack
                expected_badge_opts.pop('is_first_name_visible', None)
                expected_badge_opts.pop('is_surname_visible', None)
                expected_badge_opts.pop('is_nick_visible', None)

            if existing_badge:
                # There is an existing un-revoked badge. Check that its information is correct.
                if any(getattr(existing_badge, key) != value for (key, value) in expected_badge_opts.items()):
                    existing_badge.revoke()
                else:
                    return existing_badge, False

            if expected_badge_opts.get('personnel_class') is None:
                # They should not have a badge.
                return None, False

            badge_opts = dict(new_badge_opts, person=person)

            badge = cls(**badge_opts)
            badge.save()

            return badge, True

    @classmethod
    def get_csv_fields(cls, event):
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
        return self.personnel_class.name if self.personnel_class else ''

    @property
    def event(self):
        return self.personnel_class.event

    @property
    def meta(self):
        return self.event.badges_event_meta

    @property
    def signup(self):
        from labour.models import Signup

        if self.person is None:
            return None

        return Signup.objects.filter(event=self.event, person=self.person).first()

    @property
    def signup_extra(self):
        if not hasattr(self, '_signup_extra'):
            if self.person_id is None or self.event.labour_event_meta is None:
                self._signup_extra = None
            else:
                SignupExtra = self.event.labour_event_meta.signup_extra_model

                try:
                    self._signup_extra = SignupExtra.get_for_event_and_person(self.event, self.person)
                except SignupExtra.DoesNotExist:
                    self._signup_extra = None

        return self._signup_extra

    @property
    def event_name(self):
        return self.personnel_class.event.name if self.personnel_class else ''

    def get_printable_text(self, fields):
        return '\n'.join(str(value) for value in self.get_csv_row(self.event, fields, 'comma_separated'))

    def to_html_print(self):
        def format_name_field(value, is_visible):
            if is_visible:
                return '<strong>{value}</strong>'.format(value=escape(value))
            else:
                return escape(value)

        vars = dict(
            surname=format_name_field(self.surname.strip(), self.is_surname_visible),
            first_name=format_name_field(self.first_name.strip(), self.is_first_name_visible),
            nick=format_name_field(self.nick.strip(), self.is_nick_visible),
        )

        if self.nick:
            return "{surname}, {first_name}, {nick}".format(**vars)
        else:
            return "{surname}, {first_name}".format(**vars)

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
            return '{self.first_name} "{self.nick}" {self.surname}'.format(self=self)
        else:
            return '{self.first_name} {self.surname}'.format(self=self)
    admin_get_full_name.short_description = _('Name')
    admin_get_full_name.admin_order_field = ('surname', 'first_name', 'nick')

    def __str__(self):
        return "{person_name} ({personnel_class_name}, {event_name})".format(
            person_name=self.admin_get_full_name(),
            personnel_class_name=self.personnel_class_name,
            event_name=self.event_name,
        )
