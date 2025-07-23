from __future__ import annotations

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import ContactEmailMixin, Event, EventMetaBase, contact_email_validator
from kompassi.core.utils import alias_property, is_within_period

SCHEDULE_LAYOUT_CHOICES = [
    ("reasonable", _("Reasonable")),
    ("full_width", _("Full-width")),
]

GROUP_VERBOSE_NAMES_BY_SUFFIX = dict(
    admins="Ohjelmavastaavat",
    hosts="Kaikki ohjelmanjärjestäjät (odottavat ja hyväksytyt)",
    live="Hyväksyttyjen ohjelmien järjestäjät",
    new="Hyväksyntää odottavat ohjelmanjärjestäjät",
)


class ProgrammeEventMeta(ContactEmailMixin, EventMetaBase):
    public_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ohjelmakartan julkaisuaika",
        help_text="Ohjelmakartta näkyy kansalle tästä eteenpäin.",
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        validators=[contact_email_validator],
        verbose_name="yhteysosoite",
        help_text="Kaikki ohjelmajärjestelmän lähettämät sähköpostiviestit lähetetään tästä "
        "osoitteesta, ja tämä osoite näytetään ohjelmanjärjestäjälle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.",
    )

    accepting_cold_offers_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Accepting cold offers from"),
    )

    accepting_cold_offers_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Accepting cold offers until"),
    )

    schedule_layout = models.CharField(
        max_length=max(len(choice[0]) for choice in SCHEDULE_LAYOUT_CHOICES),
        default="reasonable",
        choices=SCHEDULE_LAYOUT_CHOICES,
        verbose_name=_("Schedule layout"),
        help_text=_(
            "Some events may opt to make their schedule use the full width of the browser window. "
            "This option selects between reasonable width (the default) and full width."
        ),
    )

    paikkala_default_max_tickets_per_batch = models.IntegerField(default=5)
    paikkala_default_max_tickets_per_user = models.IntegerField(default=5)

    override_schedule_link = models.URLField(
        blank=True,
        verbose_name=_("Override schedule link"),
        help_text=_(
            "If you have a separate programme system, you can link to it here. "
            "This link will replace the link to the internal programme schedule."
        ),
    )

    use_cbac = True

    # if set, would get copies of all programme messages
    monitor_email = None

    def __init__(self, *args, **kwargs):
        if "public" in kwargs:
            public = kwargs.pop("public")
            if public:
                kwargs["public_from"] = now()

        super().__init__(*args, **kwargs)

    def get_special_programmes(self, include_unpublished=False, **extra_criteria):
        from .programme import Programme
        from .room import Room

        schedule_rooms = Room.objects.filter(view_rooms__view__event=self.event).only("id")
        criteria = dict(category__event=self.event, **extra_criteria)
        if not include_unpublished:
            criteria.update(state="published")
        return Programme.objects.filter(**criteria).exclude(room__in=schedule_rooms)

    @classmethod
    def get_or_create_dummy(cls, event: Event | None = None):
        from django.utils.timezone import now

        from kompassi.core.models import Event

        event, unused = Event.get_or_create_dummy()
        (admin_group,) = cls.get_or_create_groups(event, ["admins"])

        meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                public_from=now(),
            ),
        )

        meta.create_groups()

        return meta, created

    def create_groups(self):
        from .alternative_programme_form import AlternativeProgrammeForm
        from .category import Category

        subjects: list[str | Category | AlternativeProgrammeForm] = [
            "new",
            "hosts",
            "live",
            "rejected",
            *(Category.objects.filter(event=self.event)),
            *(AlternativeProgrammeForm.objects.filter(event=self.event)),
        ]

        return self.get_or_create_groups(self.event, subjects)

    @classmethod
    def get_or_create_groups(cls, event, subjects):
        from kompassi.mailings.models import RecipientGroup

        from .alternative_programme_form import AlternativeProgrammeForm
        from .category import Category

        suffixes = [subject if isinstance(subject, str) else subject.qualified_slug for subject in subjects]

        groups = super().get_or_create_groups(event, suffixes)

        for subject, group in zip(subjects, groups, strict=True):
            if isinstance(subject, Category):
                verbose_name = subject.title
                category = subject
                programme_form = None
            elif isinstance(subject, AlternativeProgrammeForm):
                verbose_name = subject.title
                category = None
                programme_form = subject
            else:
                if subject not in GROUP_VERBOSE_NAMES_BY_SUFFIX:
                    continue

                verbose_name = GROUP_VERBOSE_NAMES_BY_SUFFIX[subject]
                category = None
                programme_form = None

            RecipientGroup.objects.get_or_create(
                event=event,
                app_label="programme",
                group=group,
                defaults=dict(
                    programme_category=category,
                    programme_form=programme_form,
                    verbose_name=verbose_name,
                ),
            )

        return groups

    @property
    def is_public(self):
        return self.public_from is not None and now() > self.public_from

    @property
    def is_accepting_cold_offers(self):
        return is_within_period(
            self.accepting_cold_offers_from,
            self.accepting_cold_offers_until,
        )

    @property
    def is_full_width(self):
        """
        For easy iffability in templates.
        """
        return self.schedule_layout == "full-width"

    @property
    def default_role(self):
        from .role import Role

        return Role.objects.filter(personnel_class__event=self.event, is_default=True).distinct().get()

    @property
    def is_using_alternative_programme_forms(self):
        from .alternative_programme_form import AlternativeProgrammeForm

        return AlternativeProgrammeForm.objects.filter(event=self.event).exists()

    @property
    def default_alternative_programme_form(self):
        from .alternative_programme_form import AlternativeProgrammeForm

        return AlternativeProgrammeForm.objects.filter(event=self.event, slug="default").first()

    @property
    def schedule_link(self):
        if self.override_schedule_link:
            return self.override_schedule_link
        elif meta := self.event.program_v2_event_meta:
            return meta.schedule_url
        else:
            return ""

    def get_programmes_with_open_reservations(self, t=None):
        from .programme import Programme

        if t is None:
            t = now()

        return Programme.objects.filter(
            category__event=self.event,
            is_using_paikkala=True,
            is_paikkala_public=True,
            paikkala_program__reservation_start__lte=t,
            paikkala_program__reservation_end__gt=t,
        )

    @property
    def has_open_reservations(self):
        return self.get_programmes_with_open_reservations().exists()

    def publish(self):
        self.public_from = now()
        self.save()

    def unpublish(self):
        self.public_from = None
        self.save()

    public = alias_property("is_public")

    @property
    def signup_extra_model(self):
        if self.event.labour_event_meta is not None:
            return self.event.labour_event_meta.signup_extra_model
        else:
            from kompassi.labour.models import EmptySignupExtra

            return EmptySignupExtra
