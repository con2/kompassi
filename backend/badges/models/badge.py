from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property

from django.conf import settings
from django.db import connection, models, transaction
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

from core.csv_export import CsvExportMixin
from core.models.constants import NAME_DISPLAY_STYLE_FORMATS
from core.models.event import Event
from core.utils import time_bool_property
from core.utils.pkg_resources_compat import resource_string

from ..proxies.badge.privacy import BadgePrivacyAdapter
from ..utils.default_badge_factory import default_badge_factory
from .badges_event_meta import BadgesEventMeta

logger = logging.getLogger("kompassi")


@dataclass
class ArrivalsRow:
    hour: datetime | None
    arrivals: int
    cum_arrivals: int

    QUERY = resource_string(__name__, "queries/arrivals_by_hour.sql").decode()


class Badge(models.Model, CsvExportMixin):
    person_id: int | None
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Person"),
        related_name="badges",
    )

    personnel_class = models.ForeignKey(
        "labour.PersonnelClass",
        on_delete=models.CASCADE,
        verbose_name=_("Personnel class"),
        related_name="badges",
    )

    printed_separately_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Printed separately at"),
    )

    revoked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="badges_revoked",
        verbose_name=_("Revoked by"),
    )
    revoked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Revoked at"),
    )

    arrived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Arrived at"),
    )

    first_name = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_("First name"),
    )
    is_first_name_visible = models.BooleanField(
        default=True,
        verbose_name=_("Is first name visible"),
    )

    surname = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_("Surname"),
    )
    is_surname_visible = models.BooleanField(
        default=True,
        verbose_name=_("Is surname visible"),
    )

    nick = models.CharField(
        blank=True,
        max_length=1023,
        verbose_name=_("Nick name"),
        help_text=_("If you only have a single piece of information to print on the badge, use this field."),
    )
    is_nick_visible = models.BooleanField(
        default=True,
        verbose_name=_("Is nick visible"),
    )

    job_title = models.CharField(
        max_length=63,
        blank=True,
        default="",
        verbose_name=_("Job title"),
        help_text=_("Please stay civil with the job title field."),
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="badges_created",
        verbose_name=_("Created by"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )

    batch = models.ForeignKey(
        "badges.Batch",
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Printing batch"),
        on_delete=models.SET_NULL,
        related_name="badges",
    )

    perks = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Perks"),
        help_text=_("Perks for the holder of this badge"),
    )

    is_revoked = time_bool_property("revoked_at")
    is_printed = time_bool_property("printed_at")
    is_printed_separately = time_bool_property("printed_separately_at")
    is_arrived = time_bool_property("arrived_at")

    notes = models.TextField(
        default="",
        blank=True,
        verbose_name=_("Internal notes"),
        help_text=_(
            "Internal notes are only visible to the event organizer. However, if the person in question requests a transcript of records, this field is also disclosed."
        ),
    )

    @property
    def row_css_class(self):
        return "success" if self.is_arrived else ""

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
        return self.printed_at if self.printed_at is not None else ""

    @property
    def formatted_perks(self):
        return str(self.meta.emperkelator.model_validate(self.perks))

    @property
    def full_name(self):
        """
        Analogous to Person.full_name
        """
        if self.nick and self.is_nick_visible:
            style = "firstname_nick_surname"
        else:
            style = "firstname_surname"

        return NAME_DISPLAY_STYLE_FORMATS[style].format(self=self)

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
        if not person:
            raise AssertionError("person is not set")

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

            if existing_badge:
                # There is an existing un-revoked badge. Check that its information is correct.
                if any(getattr(existing_badge, key) != value for (key, value) in expected_badge_opts.items()):
                    # The badge information is out of date. Revoke the badge and create a new one.
                    existing_badge.revoke()
                else:
                    # The badge information is up-to-date.
                    # Perks are not printed on the badge, so no need to reprint the badge on perks change.
                    existing_badge.reemperkelate()

                    return existing_badge, False

            if expected_badge_opts.get("personnel_class") is None:
                # They should not have a badge.
                return None, False

            badge = cls(person=person, **new_badge_opts)
            badge.save()

            return badge, True

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        if not update_fields or "perks" in update_fields:
            self.reemperkelate(commit=False)

        return super().save(*args, **kwargs)

    def reemperkelate(self, commit=True):
        """
        Refresh the perks on the badge based on the current state of the event and the person.
        """
        Emperkelator = self.meta.emperkelator
        if self.person:
            perks = Emperkelator.emperkelate(self.event, self.person)
            perks_dict = perks.model_dump()
        else:
            perks_dict = self.personnel_class.perks
            perks = Emperkelator.model_validate(perks_dict)

        if self.perks == perks_dict:
            # Up to date
            return perks, False

        # Needs refresh
        self.perks = perks_dict
        if commit:
            self.save(update_fields=["perks"])

        return perks, True

    @classmethod
    def get_csv_fields(cls, event):
        return [
            (cls, "personnel_class_name"),
            (BadgePrivacyAdapter, "surname"),
            (BadgePrivacyAdapter, "first_name"),
            (BadgePrivacyAdapter, "nick"),
            (BadgePrivacyAdapter, "nick_or_first_name"),
            (BadgePrivacyAdapter, "surname_or_full_name"),
            (cls, "job_title"),
        ]

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
        return self.personnel_class.name if self.personnel_class else ""

    @property
    def event(self):
        return self.personnel_class.event

    @property
    def meta(self) -> BadgesEventMeta:
        return self.event.badges_event_meta

    @property
    def signup(self):
        from labour.models import Signup

        if self.person is None:
            return None

        return Signup.objects.filter(event=self.event, person=self.person).first()

    def get_signup_extra(self):
        if self.person_id is None or self.event.labour_event_meta is None:
            return None

        SignupExtra = self.event.labour_event_meta.signup_extra_model
        if SignupExtra is None:
            return None

        try:
            return SignupExtra.get_for_event_and_person(self.event, self.person)
        except SignupExtra.DoesNotExist:
            return None

    @property
    def signup_extra(self):
        if not hasattr(self, "_signup_extra"):
            self._signup_extra = self.get_signup_extra()

        return self._signup_extra

    @property
    def event_name(self):
        return self.personnel_class.event.name if self.personnel_class else ""

    def get_printable_text(self, fields):
        return "\n".join(str(value) for value in self.get_csv_row(self.event, fields, "comma_separated"))

    def to_html_print(self):
        def format_name_field(value, is_visible):
            if is_visible:
                return f"<strong>{escape(value)}</strong>"
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
        if self.is_revoked:
            raise AssertionError("Already revoked")

        if self.is_printed_separately or self.batch:
            self.is_revoked = True
            self.revoked_by = user
            self.save()
            return self
        else:
            self.delete()
            return None

    def unrevoke(self):
        if not self.is_revoked:
            raise AssertionError("Not revoked")
        self.is_revoked = False
        self.revoked_by = None
        self.save()
        return self

    def admin_get_full_name(self):
        if self.nick:
            return f'{self.first_name} "{self.nick}" {self.surname}'
        else:
            return f"{self.first_name} {self.surname}"

    admin_get_full_name.short_description = _("Name")
    admin_get_full_name.admin_order_field = ("surname", "first_name", "nick")

    def __str__(self):
        return f"{self.admin_get_full_name()} ({self.personnel_class_name}, {self.event_name})"

    @staticmethod
    def get_arrivals_by_hour(event: Event | str):
        event_slug = event if isinstance(event, str) else event.slug

        with connection.cursor() as cursor:
            cursor.execute(ArrivalsRow.QUERY, [event_slug])
            # TODO backfill missing hours
            return [ArrivalsRow(*row) for row in cursor.fetchall()]

    @cached_property
    def _shirt_size(self):
        if perks_shirt_size := self.perks.get("shirt_size"):
            return perks_shirt_size
        elif self.signup_extra and hasattr(self.signup_extra, "shirt_size"):
            return self.signup_extra.get_shirt_size_display()
        else:
            return "Ei paitaa"

    @property
    def shirt_size(self):
        if self._shirt_type == "Ei paitaa" or self._shirt_size == "Ei paitaa":
            return ""

        return self._shirt_size

    @cached_property
    def _shirt_type(self):
        if perks_shirt_type := self.perks.get("shirt_type"):
            return perks_shirt_type
        elif self.signup_extra and hasattr(self.signup_extra, "shirt_type"):
            return self.signup_extra.get_shirt_type_display()
        else:
            return "Ei paitaa"

    @property
    def shirt_type(self):
        if self._shirt_size == "Ei paitaa":
            return "Ei paitaa"

        return self._shirt_type
