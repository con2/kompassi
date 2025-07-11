from __future__ import annotations

import logging
from collections import OrderedDict
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

import django.utils.timezone
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from core.csv_export import CsvExportMixin
from core.models import Event, Person
from core.utils import (
    alias_property,
    ensure_user_group_membership,
    get_previous_and_next,
    time_bool_property,
)

from .constants import (
    JOB_TITLE_LENGTH,
    NUM_FIRST_CATEGORIES,
    SIGNUP_STATE_BUTTON_CLASSES,
    SIGNUP_STATE_DESCRIPTIONS,
    SIGNUP_STATE_GROUPS,
    SIGNUP_STATE_IMPERATIVES,
    SIGNUP_STATE_LABEL_CLASSES,
    SIGNUP_STATE_NAMES,
    STATE_FLAGS_BY_NAME,
    STATE_NAME_BY_FLAGS,
    STATE_TIME_FIELDS,
)
from .job_category import JobCategory
from .personnel_class import PersonnelClass

if TYPE_CHECKING:
    from .roster import Shift

logger = logging.getLogger("kompassi")


@dataclass
class StateTransition:
    """
    This class represents a potential state transition of a Signup from its current state to
    another. The state transition is illustrated by a color (a CSS class) and a piece of text in the
    imperative form.

    Furthermore, we may want to disable some transitions that would otherwise be legal. These cases
    warrant an explanation to the user.

    These state transitions will be represented by buttons on the State tab of the admin signup view.
    """

    signup: Signup
    to_state: str
    disabled_reason: str = ""

    def __post_init__(self):
        self.disabled_reason = self._determine_disabled_reason()

    @property
    def from_state(self):
        return self.signup.state

    @property
    def css_class(self):
        return SIGNUP_STATE_BUTTON_CLASSES[self.to_state]

    @property
    def text(self):
        return SIGNUP_STATE_IMPERATIVES[self.to_state]

    def _determine_disabled_reason(self):
        # XXX In the Grand Order, the first flag is `is_active`.
        # If the worker would end up in an inactive state, they must not have shifts.
        if not STATE_FLAGS_BY_NAME[self.to_state][0] and self.signup.shifts.exists():
            return _("This signup has shifts. Please remove the shifts before cancelling or rejecting the signup.")

        return ""

    @property
    def is_disabled(self):
        return bool(self.disabled_reason)


class SignupMixin:
    """
    Contains functionality common to both Signup and ArchivedSignup.
    """

    state: str
    is_more_categories: bool
    # is_accepted: bool
    job_category_accepted: models.QuerySet[JobCategory]
    # personnel_classes: models.QuerySet[PersonnelClass]

    @property
    def job_category_accepted_labels(self):
        state = self.state
        label_class = SIGNUP_STATE_LABEL_CLASSES[state]

        if state == "new":
            label_texts = [cat.name for cat in self.get_first_categories()]  # type: ignore
            labels = [(label_class, label_text, None) for label_text in label_texts]

            if self.is_more_categories:
                labels.append((label_class, "...", self.get_redacted_category_names()))  # type: ignore

        elif state == "cancelled":
            labels = [(label_class, "Peruutettu", None)]

        elif state == "rejected":
            labels = [(label_class, "Hylätty", None)]

        elif state == "beyond_logic":
            labels = [(label_class, "Perätilassa", None)]

        elif self.is_accepted:  # type: ignore
            label_texts = [cat.name for cat in self.job_categories_accepted.all()]  # type: ignore
            labels = [(label_class, label_text, None) for label_text in label_texts]

        else:
            logger.warning("Unknown state: %s", state)
            labels = []

        return labels

    @property
    def personnel_class_labels(self):
        label_texts = [pc.name for pc in self.personnel_classes.all()]  # type: ignore
        return [("label-default", label_text, None) for label_text in label_texts]

    @property
    def formatted_state(self):
        return dict(SIGNUP_STATE_NAMES).get(self.state, "")

    @property
    def job_categories_label(self):
        if self.state == "new":
            return "Haetut tehtävät"
        else:
            return "Hyväksytyt tehtävät"

    @property
    def state_label_class(self):
        return SIGNUP_STATE_LABEL_CLASSES[self.state]

    @property
    def state_description(self):
        return SIGNUP_STATE_DESCRIPTIONS.get(self.state, "")


class Signup(CsvExportMixin, SignupMixin, models.Model):
    id: int

    person = models.ForeignKey("core.Person", on_delete=models.CASCADE, related_name="signups")
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)

    personnel_classes = models.ManyToManyField(
        "labour.PersonnelClass",
        blank=True,
        verbose_name="Henkilöstöluokat",
        help_text="Mihin henkilöstöryhmiin tämä henkilö kuuluu? Henkilö saa valituista ryhmistä "
        "ylimmän mukaisen badgen.",
    )

    job_categories = models.ManyToManyField(
        JobCategory,
        verbose_name="Haettavat tehtävät",
        help_text="Valitse kaikki ne tehtävät, joissa olisit valmis työskentelemään "
        "tapahtumassa. Huomaathan, että sinulle tarjottavia tehtäviä voi rajoittaa se, "
        "mitä pätevyyksiä olet ilmoittanut sinulla olevan. Esimerkiksi järjestyksenvalvojaksi "
        "voivat ilmoittautua ainoastaan JV-kortilliset.",
        related_name="signup_set",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Käsittelijän merkinnät",
        help_text=(
            "Tämä kenttä ei normaalisti näy henkilölle itselleen, mutta jos tämä "
            "pyytää henkilörekisteriotetta, kentän arvo on siihen sisällytettävä."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Luotu")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Päivitetty")

    job_categories_accepted = models.ManyToManyField(
        JobCategory,
        blank=True,
        related_name="accepted_signups",
        verbose_name="Hyväksytyt tehtäväalueet",
        help_text="Tehtäväalueet, joilla hyväksytty vapaaehtoistyöntekijä tulee työskentelemään. "
        "Tämän perusteella henkilölle mm. lähetetään oman tehtäväalueensa työvoimaohjeet. "
        "Harmaalla merkityt tehtäväalueet ovat niitä, joihin hakija ei ole itse hakenut.",
    )

    job_categories_rejected = models.ManyToManyField(
        JobCategory,
        blank=True,
        related_name="+",
        verbose_name=_("Rejected job categories"),
        help_text=_(
            "The workforce manager may use this field to inform other workforce managers that "
            "this applicant will not be accepted to a certain job category. This field is not visible "
            "to the applicant, but should they request a record of their own information, this field will "
            "be included."
        ),
    )

    xxx_interim_shifts = models.TextField(
        blank=True,
        null=True,
        default="",
        verbose_name="Työvuorot",
        help_text=(
            "Tämä tekstikenttä on väliaikaisratkaisu, jolla vänkärin työvuorot voidaan "
            "merkitä Kompassiin ja lähettää vänkärille työvoimaviestissä jo ennen kuin "
            "lopullinen työvuorotyökalu on käyttökunnossa."
        ),
    )

    alternative_signup_form_used = models.ForeignKey(
        "labour.AlternativeSignupForm",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Ilmoittautumislomake",
        help_text=(
            "Tämä kenttä ilmaisee, mitä ilmoittautumislomaketta hakemuksen täyttämiseen käytettiin. "
            "Jos kenttä on tyhjä, käytettiin oletuslomaketta."
        ),
    )

    job_title = models.CharField(
        max_length=JOB_TITLE_LENGTH,
        blank=True,
        default="",
        verbose_name="Tehtävänimike",
        help_text=(
            "Printataan badgeen ym. Asetetaan automaattisesti hyväksyttyjen tehtäväalueiden perusteella, "
            "mikäli kenttä jätetään tyhjäksi."
        ),
    )

    is_active = models.BooleanField(verbose_name="Aktiivinen", default=True)

    time_accepted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hyväksytty",
    )

    time_confirmation_requested = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Vahvistusta vaadittu",
    )

    time_finished = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Vuorot valmiit",
    )

    time_complained = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Vuoroista reklamoitu",
    )

    time_cancelled = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Peruutettu",
    )

    time_rejected = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hylätty",
    )

    time_arrived = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Saapunut tapahtumaan",
    )

    time_work_accepted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Työpanos hyväksytty",
    )

    time_reprimanded = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Työpanoksesta esitetty moite",
    )

    override_working_hours = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Aseta työtunnit käsin",
        help_text=(
            "Huomioidaan työvoimaetujen laskennassa, jos tapahtuma antaa työvoimaedut työntuntien perusteella. "
            "Jos henkilö tekee tapahtuman eteen töitä, joita ei ole huomioitu Kompassiin kirjatuissa työvuoroissa, "
            "voit asettaa tähän hänen kokonaistuntimääränsä, ja työvoimaedut lasketaan tämän mukaan."
        ),
    )

    override_formatted_perks = models.TextField(
        blank=True,
        default="",
        verbose_name="Aseta edut käsin",
        help_text="Voit tässä ylikirjoittaa, mitä tälle henkilölle näytetään sisäänkirjausnäkymän Edut-sarakkeessa.",
    )

    is_accepted = time_bool_property("time_accepted")
    is_confirmation_requested = time_bool_property("time_confirmation_requested")
    is_finished = time_bool_property("time_finished")
    is_complained = time_bool_property("time_complained")
    is_cancelled = time_bool_property("time_cancelled")
    is_rejected = time_bool_property("time_rejected")
    is_arrived = time_bool_property("time_arrived")
    is_work_accepted = time_bool_property("time_work_accepted")
    is_workaccepted = alias_property("is_work_accepted")  # for automagic groupiness
    is_reprimanded = time_bool_property("time_reprimanded")

    is_new = property(lambda self: self.state == "new")
    is_applicants = alias_property("is_active")  # group is called applicants for historical purposes
    is_confirmation = alias_property("is_confirmation_requested")
    is_processed = property(lambda self: self.state != "new")
    is_alive = property(lambda self: self.is_active and self.is_accepted and not self.is_cancelled)

    shifts: models.QuerySet[Shift]

    class Meta:
        verbose_name = _("signup")
        verbose_name_plural = _("signups")

    def __str__(self):
        p = self.person.full_name if self.person else "None"
        e = self.event.name if self.event else "None"

        return f"{p} / {e}"

    @property
    def working_hours(self):
        if self.override_working_hours is not None:
            return self.override_working_hours

        return sum((shift.hours for shift in self.shifts.all()), 0)

    @property
    def personnel_class(self):
        """
        The highest personnel class of this Signup (possibly None).
        """
        return self.personnel_classes.first()

    @property
    def signup_extra_model(self):
        return self.event.labour_event_meta.signup_extra_model

    @cached_property
    def signup_extra(self):
        SignupExtra = self.signup_extra_model
        return SignupExtra.for_signup(self) if SignupExtra else None

    def get_first_categories(self):
        return self.job_categories.all()[:NUM_FIRST_CATEGORIES]

    @property
    def is_more_categories(self):
        return self.job_categories.count() > NUM_FIRST_CATEGORIES

    def get_redacted_category_names(self):
        return ", ".join(cat.name for cat in self.job_categories.all()[NUM_FIRST_CATEGORIES:])

    @property
    def some_accepted_job_category(self) -> JobCategory:
        jc = self.job_categories_accepted.first()

        if jc is None:
            raise JobCategory.DoesNotExist("Signup has no job categories")

        return jc

    @property
    def some_job_title(self):
        """
        Tries to figure a job title for this worker using the following methods in this order

        1. A manually set job title
        2. The title of the job category the worker is accepted into
        3. A generic job title
        """

        if self.job_title:
            return self.job_title
        elif self.job_categories_accepted.exists():
            return self.some_accepted_job_category.name
        else:
            return "Työvoima"

    @property
    def has_work_reference(self):
        if (
            self.is_arrived
            and not self.is_reprimanded
            and (self.event.end_time is None or django.utils.timezone.now() > self.event.end_time)
        ):
            return self.event.labour_event_meta.work_certificate_pdf_project is not None
        return False

    @property
    def granted_privileges(self):
        if "access" not in settings.INSTALLED_APPS:
            return []

        from access.models import GrantedPrivilege

        return GrantedPrivilege.objects.filter(
            person=self.person,
            privilege__group_privileges__group__in=self.person.user.groups.all(),
            privilege__group_privileges__event=self.event,
        )

    @property
    def potential_privileges(self):
        if "access" not in settings.INSTALLED_APPS:
            return []

        from access.models import Privilege

        return Privilege.get_potential_privileges(person=self.person, group_privileges__event=self.event)

    @property
    def ordered_shifts(self):
        return self.shifts.order_by("start_time")

    @classmethod
    def get_or_create_dummy(
        cls,
        accepted=False,
        person: Person | None = None,
        event: Event | None = None,
        override_working_hours: int | None = None,
        job_category: JobCategory | None = None,
        personnel_class: PersonnelClass | None = None,
    ):
        if person is None:
            person, _ = Person.get_or_create_dummy()

        if event is None:
            event, _ = Event.get_or_create_dummy()

        if personnel_class is None:
            personnel_class, _ = PersonnelClass.get_or_create_dummy(event=event, app_label="labour")

        if job_category is None:
            job_category, _ = JobCategory.get_or_create_dummy(event=event, personnel_class=personnel_class)

        signup, created = Signup.objects.get_or_create(
            person=person,
            event=event,
            override_working_hours=override_working_hours,
        )
        if created:
            signup.job_categories.set([job_category])

        if accepted:
            signup.job_categories_accepted.set(signup.job_categories.all())

            job_category = signup.job_categories_accepted.first()
            if job_category is None:
                raise AssertionError("signup is accepted but it has no job_categories_accepted (this shouldn't happen)")

            signup.personnel_classes.add(job_category.personnel_classes.first())
            signup.state = "accepted"
            signup.save()
            signup.apply_state()

        return signup, created

    @classmethod
    def get_state_query_params(cls, state):
        flag_values = STATE_FLAGS_BY_NAME[state]
        if len(STATE_TIME_FIELDS) != len(flag_values):
            raise ValueError("STATE_TIME_FIELDS and STATE_FLAGS_BY_NAME are out of sync")

        query_params = []

        for time_field_name, flag_value in zip(STATE_TIME_FIELDS, flag_values, strict=True):
            time_field_preposition = f"{time_field_name}__isnull"
            query_params.append((time_field_preposition, not flag_value))

        # First state flag is not a time bool field, but an actual bona fide boolean field.
        # Also "is null" semantics mean that flag values are flipped, so we need to backflip it.
        query_params[0] = ("is_active", not query_params[0][1])

        return OrderedDict(query_params)

    @classmethod
    def mass_reject(cls, signups):
        return cls._mass_state_change("new", "rejected", signups)

    @classmethod
    def mass_request_confirmation(cls, signups):
        return cls._mass_state_change("accepted", "confirmation", signups)

    @classmethod
    def filter_signups_for_mass_send_shifts(cls, signups):
        return signups.filter(**cls.get_state_query_params("accepted")).exclude(
            xxx_interim_shifts="",
            shifts__isnull=True,
        )

    @classmethod
    def mass_send_shifts(cls, signups):
        return cls._mass_state_change(
            old_state="accepted",
            new_state="finished",
            signups=signups,
            filter_func=cls.filter_signups_for_mass_send_shifts,
        )

    @classmethod
    def _mass_state_change(cls, old_state, new_state, signups, filter_func=None):
        if filter_func is None:
            signups = signups.filter(**Signup.get_state_query_params(old_state))
        else:
            signups = filter_func(signups)

        for signup in signups:
            signup.state = new_state
            signup.save()
            signup.apply_state()

        return signups

    def apply_state(self):
        from ..tasks import signup_apply_state

        self.apply_state_sync()
        signup_apply_state.delay(self.pk)  # type: ignore

    def apply_state_sync(self):
        self.apply_state_ensure_job_categories_accepted_is_set()
        self.apply_state_ensure_personnel_class_is_set()

        if self.signup_extra is not None:
            self.signup_extra.apply_state()

        self.apply_state_create_badges()

    def _apply_state(self):
        self.apply_state_group_membership()
        self.apply_state_email_aliases()
        self.apply_state_send_messages()
        self.apply_state_cleanup_team_membership()

    def apply_state_group_membership(self):
        from .job_category import JobCategory
        from .personnel_class import PersonnelClass

        groups_to_add = set()
        groups_to_remove = set()

        for group_suffix in SIGNUP_STATE_GROUPS:
            should_belong_to_group = getattr(self, f"is_{group_suffix}")
            group = self.event.labour_event_meta.get_group(group_suffix)

            if should_belong_to_group:
                groups_to_add.add(group)
            else:
                groups_to_remove.add(group)

        for job_category in JobCategory.objects.filter(event=self.event):
            should_belong_to_group = self.job_categories_accepted.filter(pk=job_category.pk).exists()
            group = self.event.labour_event_meta.get_group(job_category.slug)

            if should_belong_to_group:
                groups_to_add.add(group)
            else:
                groups_to_remove.add(group)

        for personnel_class in PersonnelClass.objects.filter(event=self.event, app_label="labour"):
            should_belong_to_group = self.personnel_classes.filter(pk=personnel_class.pk).exists()
            group = self.event.labour_event_meta.get_group(personnel_class.slug)

            if should_belong_to_group:
                groups_to_add.add(group)
            else:
                groups_to_remove.add(group)

        ensure_user_group_membership(self.person.user, groups_to_add, groups_to_remove)

    def apply_state_email_aliases(self):
        if "access" not in settings.INSTALLED_APPS:
            return

        from access.models import GroupEmailAliasGrant

        GroupEmailAliasGrant.ensure_aliases(self.person)

    def apply_state_send_messages(self, resend=False):
        from mailings.models import Message

        Message.send_messages(self.event, "labour", self.person)

    def apply_state_ensure_job_categories_accepted_is_set(self):
        if self.is_accepted and not self.job_categories_accepted.exists() and self.job_categories.count() == 1:
            self.job_categories_accepted.add(self.job_categories.get())

    def apply_state_ensure_personnel_class_is_set(self):
        for app_label in self.job_categories_accepted.values_list("app_label", flat=True).distinct():
            if self.personnel_classes.filter(app_label=app_label).exists():
                continue

            personnel_class = self.some_accepted_job_category.personnel_classes.first()
            self.personnel_classes.add(personnel_class)

    def apply_state_create_badges(self):
        if self.event.badges_event_meta is None:
            return

        from badges.models import Badge

        Badge.ensure(event=self.event, person=self.person)

    def apply_state_cleanup_team_membership(self):
        """
        When an organizer quits, make sure they are removed from Intra team listing as well.
        """
        from access.models import CBACEntry
        from core.utils import ensure_user_is_member_of_group
        from intra.models.team_member import TeamMember

        event: Event = self.event

        if (meta := event.intra_event_meta) is None:
            return

        if self.person.user in meta.organizer_group.user_set.all():
            return

        TeamMember.objects.filter(person=self.person, team__event=self.event).delete()

        for app_label in meta.get_active_apps():
            ensure_user_is_member_of_group(self.person.user, event.get_app_event_meta(app_label).admin_group, False)

        CBACEntry.ensure_admin_group_privileges_for_event(event)

    def get_previous_and_next_signup(self):
        queryset = self.event.signup_set.order_by("person__surname", "person__first_name", "id").all()
        return get_previous_and_next(queryset, self)

    @property
    def _state_flags(self):
        # The Grand Order is defined here.
        return (
            self.is_active,
            self.is_accepted,
            self.is_confirmation_requested,
            self.is_finished,
            self.is_complained,
            self.is_arrived,
            self.is_work_accepted,
            self.is_reprimanded,
            self.is_rejected,
            self.is_cancelled,
        )

    @_state_flags.setter
    def _state_flags(self, flags):
        # These need to be in the Grand Order.
        (
            self.is_active,
            self.is_accepted,
            self.is_confirmation_requested,
            self.is_finished,
            self.is_complained,
            self.is_arrived,
            self.is_work_accepted,
            self.is_reprimanded,
            self.is_rejected,
            self.is_cancelled,
        ) = flags

    @property
    def state(self):
        return STATE_NAME_BY_FLAGS[self._state_flags]  # type: ignore

    @state.setter
    def state(self, new_state):
        self._state_flags = STATE_FLAGS_BY_NAME[new_state]

    @property
    def next_states(self):
        cur_state = self.state

        states = []

        if cur_state == "new":
            states.extend(("accepted", "rejected", "cancelled"))
        elif cur_state == "accepted":
            states.extend(("finished", "confirmation", "cancelled"))
        elif cur_state == "confirmation":
            states.extend(("accepted", "cancelled"))
        elif cur_state == "finished":
            states.extend(("arrived", "complained", "no_show", "relieved"))
        elif cur_state == "complained":
            states.extend(("finished", "relieved"))
        elif cur_state == "arrived":
            states.extend(("honr_discharged", "dish_discharged", "relieved"))
        elif cur_state == "beyond_logic":
            states.extend(
                (
                    "new",
                    "accepted",
                    "finished",
                    "complained",
                    "rejected",
                    "cancelled",
                    "arrived",
                    "honr_discharged",
                    "no_show",
                )
            )

        if cur_state != "beyond_logic":
            states.append("beyond_logic")

        return states

    @property
    def next_states_buttons(self):
        return [StateTransition(self, to_state) for to_state in self.next_states]

    @property
    def state_times(self):
        return [
            (
                self._meta.get_field(field_name).verbose_name,
                getattr(self, field_name, None),
            )
            for field_name in STATE_TIME_FIELDS
            if getattr(self, field_name, None)
        ]

    @property
    def person_messages(self):
        if getattr(self, "_person_messages", None) is None:
            self._person_messages = self.person.personmessage_set.filter(
                message__recipient__event=self.event,
                message__recipient__app_label="labour",
            ).order_by("-created_at")

        return self._person_messages

    @property
    def have_person_messages(self):
        return self.person_messages.exists()

    @property
    def applicant_has_actions(self):
        return any(
            [
                self.applicant_can_edit,
                self.applicant_can_confirm,
                self.applicant_can_cancel,
            ]
        )

    @property
    def applicant_can_edit(self):
        return self.state == "new" and self.is_registration_open

    @property
    def is_registration_open(self):
        if self.alternative_signup_form_used is not None:
            return self.alternative_signup_form_used.is_active
        else:
            return self.event.labour_event_meta.is_registration_open

    @property
    def applicant_can_confirm(self):
        return self.state == "confirmation"

    def confirm(self):
        if self.state != "confirmation":
            raise ValueError(f"Must be in state 'confirmation' to confirm, not {self.state}")

        self.state = "accepted"
        self.save()
        self.apply_state()

    @property
    def applicant_can_cancel(self):
        return self.is_active and not self.is_cancelled and not self.is_rejected and not self.is_arrived

    @property
    def formatted_personnel_classes(self):
        from .job_category import format_job_categories

        return format_job_categories(self.personnel_classes.all())

    @property
    def formatted_job_categories_accepted(self):
        from .job_category import format_job_categories

        return format_job_categories(self.job_categories_accepted.all())

    @property
    def formatted_job_categories(self):
        from .job_category import format_job_categories

        return format_job_categories(self.job_categories.all())

    @property
    def formatted_shifts(self):
        parts = []

        if self.xxx_interim_shifts:
            parts.append(self.xxx_interim_shifts)

        parts.extend(str(shift) for shift in self.shifts.all().order_by("start_time"))

        return "\n\n".join(part for part in parts if part)

    # for admin
    @property
    def full_name(self):
        return self.person.full_name

    @property
    def info_links(self):
        from .info_link import InfoLink

        return InfoLink.objects.filter(
            event=self.event,
            group__user=self.person.user,
        )

    @property
    def email_address(self):
        from access.models import EmailAlias

        email_alias = (
            EmailAlias.objects.filter(
                type__domain__organization=self.event.organization,
                person=self.person,
            )
            .order_by("type__priority")
            .first()
        )  # TODO order

        return email_alias.email_address if email_alias else self.person.email

    @classmethod
    def get_csv_fields(cls, event):
        if getattr(event, "_signup_csv_fields", None) is None:
            from core.models import Person

            event._signup_csv_fields = []

            related_models = [Person, Signup]

            fields_to_skip = [
                # useless & non-serializable
                (Person, "user"),
                (Signup, "person"),
                # too official
                (Person, "official_first_names"),
                (Person, "muncipality"),
            ]

            SignupExtra = event.labour_event_meta.signup_extra_model
            if SignupExtra is not None:
                related_models.append(SignupExtra)
                fields_to_skip.extend(
                    [
                        # SignupExtraBase ("V2")
                        (SignupExtra, "event"),
                        (SignupExtra, "person"),
                        # ObsoleteSignupExtraBaseV1
                        (SignupExtra, "signup"),
                    ]
                )

            # XXX HACK jv-kortin numero
            if "labour_common_qualifications" in settings.INSTALLED_APPS:
                from labour_common_qualifications.models import JVKortti

                related_models.append(JVKortti)
                fields_to_skip.append((JVKortti, "personqualification"))

            for model in related_models:
                for field in model._meta.fields:
                    if (model, field.name) in fields_to_skip:
                        continue

                    event._signup_csv_fields.append((model, field))

                for field in model._meta.many_to_many:
                    event._signup_csv_fields.append((model, field))

        return event._signup_csv_fields

    def get_csv_related(self):
        from core.models import Person

        related = {Person: self.person}

        signup_extra_model = self.signup_extra_model
        if signup_extra_model:
            related[signup_extra_model] = self.signup_extra

        # XXX HACK jv-kortin numero
        if "labour_common_qualifications" in settings.INSTALLED_APPS:
            from labour_common_qualifications.models import JVKortti

            try:
                jv_kortti = JVKortti.objects.get(personqualification__person=self.person)
                related[JVKortti] = jv_kortti  # type: ignore
            except JVKortti.DoesNotExist:
                related[JVKortti] = None  # type: ignore

        return related

    def as_dict(self):
        # XXX?
        signup_extra = self.signup_extra

        if signup_extra is None:
            shift_wishes = ""
            total_work = ""
            shift_type = ""
        else:
            shift_wishes = signup_extra.shift_wishes if signup_extra.get_field("shift_wishes") else ""
            total_work = signup_extra.total_work if signup_extra.get_field("total_work") else ""
            shift_type = signup_extra.get_shift_type_display() if signup_extra.get_field("shift_type") else ""

        return dict(
            id=self.person.id,
            fullName=self.person.full_name,
            shiftWishes=shift_wishes,
            totalWork=total_work,
            currentlyAssigned=self.shifts.all().aggregate(sum_hours=Coalesce(Sum("hours"), 0))["sum_hours"],
            shiftType=shift_type,
        )

    @classmethod
    def for_signup(cls, signup):
        """
        Surveys make use of this method.
        """
        return signup
