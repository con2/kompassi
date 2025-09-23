from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.access.models.email_alias_domain import EmailAliasDomain
from kompassi.access.models.email_alias_type import EmailAliasVariant
from kompassi.access.models.group_email_alias_grant import GroupEmailAliasGrant
from kompassi.badges.models import BadgesEventMeta
from kompassi.core.models import Event, Organization, Venue
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.forms.models.survey import SurveyDTO
from kompassi.intra.models import IntraEventMeta, Team
from kompassi.involvement.models.involvement_to_badge import InvolvementToBadgeMapping
from kompassi.involvement.models.involvement_to_group import InvolvementToGroupMapping
from kompassi.involvement.models.meta import InvolvementEventMeta
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models import AlternativeSignupForm, JobCategory, LabourEventMeta, PersonnelClass, Survey
from kompassi.program_v2.models.meta import ProgramV2EventMeta

from ...models import Accommodation, KnownLanguage, SignupExtra


class Setup:
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_labour()
        self.setup_badges()
        self.setup_intra()
        self.setup_access()
        self.setup_forms()
        self.setup_program_v2()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="kotae-ry",
            defaults=dict(
                name="Kotae ry",
                homepage_url="https://www.kotae.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampereen Messu- ja Urheilukeskus")
        self.event, unused = Event.objects.get_or_create(
            slug="kotaeexpo2025",
            defaults=dict(
                name="Kotae Expo (2025)",
                name_genitive="Kotae Expon",
                name_illative="Kotae Expoon",
                name_inessive="Kotae Expossa",
                homepage_url="http://www.kotae.fi",
                organization=self.organization,
                start_time=datetime(2025, 11, 22, 10, 0, tzinfo=self.tz),
                end_time=datetime(2025, 11, 23, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Kotae Expon vapaaehtoistiimi <vapaaehtoiset@kotae.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ("Vastaava", "vastaava", "labour"),
            ("Vapaaehtoinen", "vapaaehtoinen", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "program_v2"),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        vapaaehtoinen = PersonnelClass.objects.get(event=self.event, slug="vapaaehtoinen")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        for jc_data in [
            ("vastaava", "Vastaava", "Tapahtuman järjestelytoimikunnan jäsen", [vastaava]),
            (
                "yleinen",
                "Yleisvänkäri",
                "Olet conissa niinsanottu joka puun höylä, eli tarvittaessa olet kutsuttavissa auttamaan muita tiimejä erilaisissa tehtävissä, kuten mm. vesipisteiden täytössä tai ruuhka-ajan narikassa.",
                [vapaaehtoinen],
            ),
        ]:
            slug, name, description, pcs = jc_data

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    name=name,
                    description=description,
                ),
            )

            if created:
                job_category.personnel_classes.set(pcs)

        labour_event_meta.create_groups()

        for name in ["Vastaava"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for language in [
            "Suomi",
            "Ruotsi",
            "Englanti",
            "Japani",
            "Korea",
        ]:
            KnownLanguage.objects.get_or_create(name=language)

        for accommodation_name in [
            "Pe-la väliselle yölle",
            "La-su väliselle yölle",
        ]:
            Accommodation.objects.get_or_create(name=accommodation_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                title="Vastaavien ilmoittautumislomake",
                signup_form_class_path="events.kotaeexpo2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.kotaeexpo2025.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="erikoistehtava",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.kotaeexpo2025.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.kotaeexpo2025.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Kotae Expon vastaavista on ohjeistanut sinua ilmoittautumaan tällä lomakkeella. "
                ),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="tyovuorotoiveet",
            defaults=dict(
                title="Työvuorotoiveet",
                description=(
                    "Tässä vaiheessa voit vaikuttaa työvuoroihisi. Jos saavut tapahtumaan vasta sen alkamisen "
                    "jälkeen tai sinun täytyy lähteä ennen tapahtuman loppumista, kerro se tässä. Lisäksi jos "
                    "tiedät ettet ole käytettävissä tiettyihin aikoihin tapahtuman aikana tai haluat esimerkiksi "
                    "nähdä jonkun ohjelmanumeron, kerro siitäkin. Työvuorotoiveiden toteutumista täysin ei voida "
                    "taata."
                ),
                form_class_path="events.kotaeexpo2025.forms:ShiftWishesSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=60),
            ),
        )

    def setup_badges(self):
        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=False,
            ),
        )

    def setup_access(self):
        cc_group = self.event.labour_event_meta.get_group("vastaava")
        domain = EmailAliasDomain.objects.get(domain_name="kotae.fi")
        GroupEmailAliasGrant.ensure(
            cc_group,
            domain,
            [
                EmailAliasVariant.FIRSTNAME_LASTNAME,
                EmailAliasVariant.CUSTOM,
            ],
        )

    def setup_intra(self):
        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("vastaava")
        IntraEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
                is_organizer_list_public=True,
            ),
        )

        for team_slug, team_name in [
            ("pj", "Pääjärjestäjä"),
            ("talous", "Talous"),
            ("turvallisuus", "Turvallisuus"),
            ("viestinta", "Viestintä"),
            ("markkinointi", "Markkinointi"),
            ("grafiikka", "Grafiikka"),
            ("tilat", "Tilat"),
            ("kunniavieras", "Kunniavieras"),
            ("vapaaehtoiset", "Vapaaehtoiset"),
            ("tekniikka", "Tekniikka"),
            ("taltiointi", "Taltiointi"),
            ("ohjelma", "Ohjelma"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = f"{team_slug}@kotae.fi"

            team, _ = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                    email=email,
                ),
            )

        for team in Team.objects.filter(event=self.event):
            team.is_public = True
            team.save()

    def setup_forms(self):
        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])

        FormsEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        for survey in [
            SurveyDTO(
                slug="expense-claim",
                key_fields=["title", "amount"],
                login_required=True,
                anonymity="NAME_AND_EMAIL",
                active_from=datetime(2025, 1, 1, 0, 0, tzinfo=self.tz),
                active_until=datetime(2025, 12, 31, 23, 59, tzinfo=self.tz),
            ),
        ]:
            survey.save(self.event)

    def setup_program_v2(self):
        InvolvementEventMeta.ensure(self.event)

        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])

        # TODO(Kotae Expo): Define your volunteer registry
        registry, _created = Registry.objects.get_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_fi="Kotae ry:n vapaaehtoisrekisteri",
                title_en="Volunteers of Kotae ry",
            ),
        )

        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                default_registry=registry,
                contact_email="Kotae Expon ohjelmatiimi <ohjelma@kotae.fi>",
            ),
        )

        universe = self.event.involvement_universe

        ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")
        InvolvementToBadgeMapping.objects.update_or_create(
            universe=universe,
            personnel_class=ohjelma,
            defaults=dict(
                required_dimensions={
                    "state": ["active"],
                    "type": ["program-host"],
                },
                job_title="Ohjelmanjärjestäjä",
                priority=self.get_ordering_number(),
            ),
        )

        group, _ = Group.objects.get_or_create(name=f"{self.event.slug}-program-hosts")
        InvolvementToGroupMapping.objects.get_or_create(
            universe=universe,
            required_dimensions={
                "state": ["active"],
                "type": ["program-host"],
            },
            group=group,
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Kotae Expo 2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
