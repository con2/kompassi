from datetime import timedelta
from typing import Any

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import ContactEmailMixin, Event, EventMetaBase, contact_email_validator
from kompassi.core.utils import alias_property, full_hours_between, is_within_period

from .constants import GROUP_VERBOSE_NAMES_BY_SUFFIX, SIGNUP_STATE_GROUPS


class LabourEventMeta(ContactEmailMixin, EventMetaBase):
    signup_extra_content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE)

    registration_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Registration opens"),
    )
    public_from = alias_property("registration_opens")

    registration_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Registration closes"),
    )
    public_until = alias_property("registration_closes")

    work_begins = models.DateTimeField(verbose_name="Ensimmäiset työvuorot alkavat")
    work_ends = models.DateTimeField(verbose_name="Viimeiset työvuorot päättyvät")

    monitor_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="tarkkailusähköposti",
        help_text="Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään myös tähän osoitteeseen.",
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        validators=[
            contact_email_validator,
        ],
        verbose_name="yhteysosoite",
        help_text="Kaikki työvoimajärjestelmän lähettämät sähköpostiviestit lähetetään tästä "
        "osoitteesta, ja tämä osoite näytetään työvoimalle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.",
    )

    signup_message = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Ilmoittautumisen huomautusviesti",
        help_text="Tämä viesti näytetään kaikille työvoimailmoittautumisen alussa. Käytettiin "
        "esimerkiksi Tracon 9:ssä kertomaan, että työvoimahaku on avoinna enää JV:ille ja "
        "erikoistehtäville.",
    )

    work_certificate_pdf_project = models.ForeignKey(
        "emprinten.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    work_certificate_signer = models.TextField(
        null=True,
        blank=True,
        default="",
        verbose_name="Työtodistuksen allekirjoittaja",
        help_text="Tämän kentän sisältö näkyy työtodistuksen allekirjoittajan nimenselvennyksenä. "
        "On suositeltavaa sisällyttää tähän omalle rivilleen allekirjoittajan tehtävänimike.",
    )

    use_cbac = True

    class Meta:
        verbose_name = _("labour event meta")
        verbose_name_plural = _("labour event metas")

    def __str__(self):
        return self.event.name if self.event else "None"

    @property
    def signup_extra_model(self):
        return self.signup_extra_content_type.model_class()

    @classmethod
    def events_registration_open(cls):
        from kompassi.core.models import Event

        t = now()
        return Event.objects.filter(
            laboureventmeta__registration_opens__isnull=False,
            laboureventmeta__registration_opens__lte=t,
        ).exclude(
            laboureventmeta__registration_closes__isnull=False,
            laboureventmeta__registration_closes__lte=t,
        )

    @classmethod
    def get_or_create_dummy(cls, event: Event | None = None):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Event

        from .signup_extras import EmptySignupExtra

        if event is None:
            event, unused = Event.get_or_create_dummy()

        if event.start_time is None:
            raise ValueError("Event must have a start time")
        if event.end_time is None:
            raise ValueError("Event must have an end time")

        content_type = ContentType.objects.get_for_model(EmptySignupExtra)
        (admin_group,) = LabourEventMeta.get_or_create_groups(event, ["admins"])

        t = now()

        labour_event_meta, created = cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
                work_begins=event.start_time - timedelta(days=1),
                work_ends=event.end_time + timedelta(days=1),
                contact_email="dummy@example.com",
                monitor_email="dummy@example.com",
            ),
        )

        labour_event_meta.create_groups()

        return labour_event_meta, created

    @classmethod
    def get_or_create_groups(cls, event, job_categories_or_suffixes):
        from kompassi.mailings.models import RecipientGroup

        from .job_category import JobCategory
        from .personnel_class import PersonnelClass

        suffixes = [
            jc_or_suffix if isinstance(jc_or_suffix, str) else jc_or_suffix.slug
            for jc_or_suffix in job_categories_or_suffixes
        ]

        groups = super().get_or_create_groups(event, suffixes)

        for jc_or_suffix, group in zip(job_categories_or_suffixes, groups, strict=True):
            if isinstance(jc_or_suffix, JobCategory):
                verbose_name = jc_or_suffix.name
                job_category = jc_or_suffix
                personnel_class = None
            elif isinstance(jc_or_suffix, PersonnelClass):
                verbose_name = jc_or_suffix.name
                job_category = None
                personnel_class = jc_or_suffix
            else:
                verbose_name = GROUP_VERBOSE_NAMES_BY_SUFFIX[jc_or_suffix]
                job_category = None
                personnel_class = None

            RecipientGroup.objects.get_or_create(
                event=event,
                app_label="labour",
                group=group,
                defaults=dict(
                    job_category=job_category,
                    personnel_class=personnel_class,
                    verbose_name=verbose_name,
                ),
            )

        return groups

    def create_groups_async(self):
        from ..tasks import labour_event_meta_create_groups

        labour_event_meta_create_groups.delay(self.pk)  # type: ignore

    def create_groups(self):
        from .job_category import JobCategory
        from .personnel_class import PersonnelClass

        job_categories_or_suffixes: list[Any] = list(SIGNUP_STATE_GROUPS)
        job_categories_or_suffixes.extend(JobCategory.objects.filter(event=self.event))
        job_categories_or_suffixes.extend(PersonnelClass.objects.filter(event=self.event, app_label="labour"))
        return LabourEventMeta.get_or_create_groups(self.event, job_categories_or_suffixes)

    @property
    def is_registration_open(self):
        return is_within_period(self.registration_opens, self.registration_closes)

    is_public = alias_property("is_registration_open")

    def publish(self):
        """
        Used by the start/stop signup period view to start the signup period. Returns True
        if the user needs to be warned about a certain corner case where information was lost.
        """
        warn = False

        if self.public_until and self.public_until <= now():
            self.public_until = None
            warn = True

        self.public_from = now()
        self.save()

        return warn

    def unpublish(self):
        """
        Used by the start/stop signup period view to end the signup period. We prefer setting
        public_until to clearing public_from because this causes less information loss.
        """
        self.public_until = now()
        self.save()

    def is_person_signed_up(self, person):
        return self.event.signup_set.filter(person=person).exists()

    def get_signup_for_person(self, person):
        from .signup import Signup

        try:
            return self.event.signup_set.get(person=person)
        except Signup.DoesNotExist:
            return Signup(person=person, event=self.event)

    @property
    def work_hours(self):
        return full_hours_between(self.work_begins, self.work_ends)

    @property
    def applicants_group(self):
        return self.get_group("applicants")

    @property
    def accepted_group(self):
        return self.get_group("accepted")

    @property
    def finished_group(self):
        return self.get_group("finished")

    @property
    def rejected_group(self):
        return self.get_group("rejected")
