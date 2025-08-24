from __future__ import annotations

import logging
from datetime import datetime, timedelta
from datetime import time as time_type
from decimal import Decimal

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.access.models import GroupEmailAliasGrant, GroupPrivilege, Privilege
from kompassi.access.models.email_alias_domain import EmailAliasDomain
from kompassi.access.models.email_alias_type import EmailAliasVariant
from kompassi.badges.models.badges_event_meta import BadgesEventMeta
from kompassi.badges.models.survey_to_badge import SurveyToBadgeMapping
from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.person import Person
from kompassi.core.models.venue import Venue
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.dimension_value_dto import DimensionValueDTO
from kompassi.dimensions.models.enums import ValueOrdering
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.forms.models.projection import Projection
from kompassi.forms.models.splat import Splat
from kompassi.forms.models.survey import Survey
from kompassi.intra.models import IntraEventMeta, Team
from kompassi.involvement.models.involvement_to_badge import InvolvementToBadgeMapping
from kompassi.involvement.models.involvement_to_group import InvolvementToGroupMapping
from kompassi.involvement.models.meta import InvolvementEventMeta
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models.alternative_signup_forms import AlternativeSignupForm
from kompassi.labour.models.info_link import InfoLink
from kompassi.labour.models.job_category import JobCategory
from kompassi.labour.models.labour_event_meta import LabourEventMeta
from kompassi.labour.models.personnel_class import PersonnelClass
from kompassi.labour.models.qualifications import Qualification
from kompassi.labour.models.survey import Survey as LabourSurvey
from kompassi.program_v2.models.meta import ProgramV2EventMeta
from kompassi.program_v2.models.program import Program
from kompassi.program_v2.models.schedule_item import ScheduleItem
from kompassi.program_v2.utils.backfill import backfill
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.models.product import Product
from kompassi.tickets_v2.models.quota import Quota
from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider

from ...models import Night, SignupExtra

logger = logging.getLogger(__name__)
KIRPPUTORI_KONSTI_DESCRIPTION = """
Traconin kirpputorille pääsee ostoksille pe klo 16–22 ja la klo 9:30–14 ainoastaan ajanvarauksella. Muina aikoina kirpputori palvelee asiakkaita jonosta. Ajanvaraus tapahtuu käyttäen Konstia, johon kirjaudutaan Kompassi-tunnuksilla. Molempien päivien ajanvarausajoille voi ilmoittautua alkaen pe klo 08:00. Koska halukkaita voi olla enemmän kuin kirpputorin ajanvarausaikoihin mahtuu, ajat arvotaan. Arvonnat tapahtuvat perjantaina kello 14:00 ja 17:00 sekä lauantaina kello 7:30. Kunkin arvonnan jälkeen niille ajanvarausajoille, joille on vielä tilaa, voi ilmoittautua Konstissa suoraan.

Ilmoittaudu enintään kolmeen sinulle sopivaan aikaan per arvontablokki. Jos sinua onnistaa arvonnassa, saat yhden puolen tunnin mittaisen saapumisajan jonka kuluessa voit saapua jonoon koska tahansa. Saapuessasi kirpputorille avaa lippu älypuhelimeesi ja näytä se järjestyksenvalvojalle. Lipun avaaminen onnistuu kätevimmin avaamalla älypuhelimessa osoite kirpputori.tracon.fi ja valitsemalla avautuvasta näkymästä kirpputorin ajanvarauksen kohdalta ”Avaa pääsylippu”. Huomaathan että voittamasi aika takaa pääsyn kirpputorijonoon, mutta saatat silti joutua jonottamaan kirpputorille pääsyä.

Jos haluat varata kirpputoriajan ryhmänä, teidän on ensin muodostettava ryhmä Konstin Ryhmä-näkymässä. Yksi jäsen luo ryhmän ja saa liittymiskoodin, jonka avulla muut jäsenet liittyvät ryhmään. Tämän jälkeen ryhmän perustaja ilmoittautuu arvontaan tai varaa ajan koko ryhmän puolesta. Tarkemmat ohjeet löytyvät Konstin ohjeista.

🚨 HUOM! Arvonnassa arvotaan 30 min ajanvarauksia. Voit kaikissa kolmessa arvonnassa ilmoittautua kolmeen sinulle sopivaan aikaikkunaan, ja jokaisessa arvonnassa voit päästä niistä yhteen.
""".strip()


class Setup:
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test: bool = False, dev_tickets: bool = False):
        self.test = test
        self.tz = tzlocal()
        self.dev_tickets = dev_tickets
        self.setup_core()
        self.setup_labour()
        self.setup_badges()
        self.setup_intra()
        self.setup_tickets_v2()
        self.setup_forms()
        self.setup_program_v2()
        self.setup_kirpputori()
        self.setup_access()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="tracon-ry",
            defaults=dict(
                name="Tracon ry",
                homepage_url="https://ry.tracon.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
        self.event, unused = Event.objects.get_or_create(
            slug="tracon2025",
            defaults=dict(
                name="Tracon (2025)",
                name_genitive="Traconin",
                name_illative="Traconiin",
                name_inessive="Traconissa",
                homepage_url="http://2025.tracon.fi",
                organization=self.organization,
                start_time=datetime(2025, 9, 5, 16, 0, tzinfo=self.tz),
                end_time=datetime(2025, 9, 7, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, _ = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        assert self.event.start_time
        assert self.event.end_time

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=(self.event.start_time - timedelta(days=1)).replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Traconin työvoimatiimi <tyovoima@tracon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.update_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        fmh = PersonnelClass.objects.filter(event=self.event, slug="ylivankari")
        if fmh.exists():
            fmh.update(name="Vuorovastaava", slug="vuorovastaava")

        for pc_data in [
            (
                "Coniitti",
                "coniitti",
                "labour",
            ),
            (
                "Duniitti",
                "duniitti",
                "labour",
            ),
            (
                "Vuorovastaava",
                "vuorovastaava",
                "labour",
            ),
            (
                "Työvoima",
                "tyovoima",
                "labour",
            ),
            (
                "Ohjelma",
                "ohjelma",
                "program_v2",
            ),
            (
                "Guest of Honour",
                "goh",
                "programme",
            ),
            ("Media", "media", "badges", "Badge (external)"),
            ("Myyjä", "myyja", "badges", "Myyjäranneke"),
            ("Artesaani", "artesaani", "badges", "?"),
            ("Vieras", "vieras", "badges", "Badge (external)"),
            ("Vapaalippu, viikonloppu", "vapaalippu-vkl", "tickets", "Viikonloppuranneke"),
            ("Vapaalippu, perjantai", "vapaalippu-pe", "tickets", "Perjantairanneke"),
            ("Vapaalippu, lauantai", "vapaalippu-la", "tickets", "Lauantairanneke"),
            ("Vapaalippu, sunnuntai", "vapaalippu-su", "tickets", "Sunnuntairanneke"),
            ("Cosplaykisaaja", "cosplay", "tickets", "?"),
            ("AMV-kisaaja", "amv", "tickets", "?"),
            ("Taidekuja", "taidekuja", "tickets", "?"),
            ("Taidepolku", "taidepolku", "tickets", "?"),
            ("Yhdistyspöydät", "yhdistyspoydat", "tickets", "?"),
        ]:
            if len(pc_data) == 4:
                pc_name, pc_slug, pc_app_label, _pc_perks = pc_data
            else:
                pc_name, pc_slug, pc_app_label = pc_data

            PersonnelClass.objects.update_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        # v33
        PersonnelClass.objects.filter(
            event=self.event,
            slug="coniitti",
            icon_css_class="fa-user",
        ).update(icon_css_class="fa-check-square")

        PersonnelClass.objects.filter(
            event=self.event,
            slug="duniitti",
            icon_css_class="fa-user",
        ).update(icon_css_class="fa-check-square-o")

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="tracon2018"),
                target_event=self.event,
            )

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications.set([qual])

        labour_event_meta.create_groups()

        for night in [
            "Perjantain ja lauantain välinen yö",
            "Lauantain ja sunnuntain välinen yö",
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.tracon2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.tracon2025.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for url, link_title, link_group in [
            (
                "https://wiki.tracon.fi/collection/tracon-2025-mhHLdYhJEc",
                "Coniteawiki",
                "conitea",
            ),
            (
                "https://wiki.tracon.fi/collection/traconin-tyovoimawiki-Oinc2anefS",
                "Työvoimawiki",
                "accepted",
            ),
        ]:
            InfoLink.objects.update_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=url,
                    group=labour_event_meta.get_group(link_group),
                ),
            )

        assert self.event.start_time

        LabourSurvey.objects.get_or_create(
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
                form_class_path="events.tracon2025.forms:ShiftWishesSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=60),
            ),
        )

        LabourSurvey.objects.get_or_create(
            event=self.event,
            slug="swag",
            defaults=dict(
                title="Swag",
                description=(
                    "Tarjoamme työvoimatuotteeksi joko kangaskassin tai paidan. Valitse tässä kumpi, "
                    "sekä paidan tapauksessa paitakokosi."
                ),
                form_class_path="events.tracon2025.forms:SwagSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=90),
            ),
        )

    def setup_badges(self):
        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_program_v2(self):
        InvolvementEventMeta.ensure(self.event)

        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                guide_v2_embedded_url="https://2025.tracon.fi/opas/",
                contact_email="Traconin ohjelmatiimi <ohjelma@tracon.fi>",
                default_registry=Registry.objects.get(
                    scope=self.event.organization.scope,
                    slug="volunteers",
                ),
            ),
        )
        meta.ensure()

        universe = self.event.involvement_universe

        ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")
        InvolvementToBadgeMapping.objects.update_or_create(
            universe=universe,
            personnel_class=ohjelma,
            defaults=dict(
                required_dimensions={
                    "state": ["active"],
                    "type": ["combined-perks"],
                    "v1-personnel-class": ["ohjelma"],
                },
                job_title="Ohjelmanpitäjä",
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

    def setup_kirpputori(self, slot_duration=timedelta(minutes=30)):
        meta = self.event.program_v2_event_meta
        if not meta:
            raise AssertionError("No (appease typechecker)")

        if not meta.universe.dimensions.filter(slug="konsti").exists():
            backfill(self.event)

        room_dimension = meta.universe.dimensions.get(slug="room")
        room_dimension_value, created = room_dimension.values.get_or_create(
            slug="sopraano",
            defaults=dict(title_fi="Sopraano", title_en="Sopraano"),
        )
        log_get_or_create(logger, room_dimension_value, created)

        dimensions = {
            "konsti": ["fleamarket"],
            "room": ["sopraano"],
        }
        annotations = {
            "internal:links:signup": "https://ropekonsti.fi",  # TODO
        }
        cache = meta.universe.preload_dimensions()

        for program_slug, program_title, day, start_time, end_time, max_attendance in [
            (
                "kirpputori-perjantai-alkuilta",
                "Kirpputorin ajanvaraus: Perjantai klo 16–19",
                0,
                time_type(16, 0),
                time_type(19, 0),
                100,
            ),
            (
                "kirpputori-perjantai-loppuilta",
                "Kirpputorin ajanvaraus: Perjantai klo 19–22",
                0,
                time_type(19, 0),
                time_type(22, 0),
                130,
            ),
            (
                "kirpputori-lauantai",
                "Kirpputorin ajanvaraus: Lauantai klo 9:30–14",
                1,
                time_type(9, 30),
                time_type(14, 0),
                130,
            ),
        ]:
            date = self.event.start_time + timedelta(days=day)
            prog_start_dt = datetime.combine(date, start_time, tzinfo=self.tz)
            prog_end_dt = datetime.combine(date, end_time, tzinfo=self.tz)

            program, created = Program.objects.update_or_create(
                slug=program_slug,
                event=self.event,
                defaults=dict(
                    title=program_title,
                    description=KIRPPUTORI_KONSTI_DESCRIPTION,
                    annotations=annotations,
                ),
            )
            log_get_or_create(logger, program, created)

            sched_start_dt = prog_start_dt
            while sched_start_dt < prog_end_dt:
                sched_end_dt = sched_start_dt + slot_duration
                formatted_start_dt = sched_start_dt.strftime("%H:%M")
                formatted_end_dt = sched_end_dt.strftime("%H:%M")

                sched_max_attendance = (
                    50
                    if program_slug == "kirpputori-perjantai-loppuilta" and sched_end_dt == prog_end_dt
                    else max_attendance
                )

                sched, created = ScheduleItem.objects.update_or_create(
                    program=program,
                    slug=f"{program_slug}-{formatted_start_dt.replace(':', '')}",
                    # FMH can't use .with… with get_or_create
                    defaults=dict(
                        start_time=sched_start_dt,
                        duration=slot_duration,
                        annotations={
                            "konsti:maxAttendance": sched_max_attendance,
                            "internal:subtitle": f"Saapuminen klo {formatted_start_dt}–{formatted_end_dt}",
                        },
                        cached_end_time=sched_end_dt,
                        cached_event_id=self.event.id,
                    ),
                )
                log_get_or_create(logger, sched, created)
                sched.refresh_cached_fields()

                sched_start_dt += slot_duration

            program.set_dimension_values(dimensions, cache)
            program.refresh_cached_fields()
            program.refresh_dependents()

    def setup_access(self):
        # Grant accepted workers access to Tracon Slack
        privilege = Privilege.objects.get(slug="tracon-slack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            Group.objects.get(name=f"{self.event.slug}-program-hosts"),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

        cc_group = self.event.labour_event_meta.get_group("conitea")
        domain = EmailAliasDomain.objects.get(domain_name="tracon.fi")
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
        organizer_group = self.event.labour_event_meta.get_group("conitea")
        IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("jory", "Johtoryhmä"),
            ("ohjelma", "Ohjelma"),
            ("isosali", "Iso sali"),
            ("aspa", "Asiakaspalvelu"),
            ("talous", "Talous"),
            ("tilat", "Tilat"),
            ("puisto", "Puisto"),
            ("tyovoima", "Työvoima"),
            ("tekniikka", "Tekniikka"),
            ("turva", "Turva"),
            ("video", "Videotuotanto"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = f"{team_slug}@tracon.fi"

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
            team.is_public = team.slug != "tracoff"
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
            # SurveyDTO(
            #     slug="kickoff-signup",
            #     anonymity="NAME_AND_EMAIL",
            #     max_responses_per_user=1,
            #     login_required=True,
            # ),
            # SurveyDTO(
            #     slug="expense-claim",
            #     key_fields=["title", "amount"],
            #     login_required=True,
            #     anonymity="NAME_AND_EMAIL",
            # ),
            # SurveyDTO(
            #     slug="car-usage",
            #     key_fields=["title", "kilometers"],
            #     login_required=True,
            #     anonymity="NAME_AND_EMAIL",
            # ),
        ]:
            survey.save(self.event)

        survey = Survey.objects.filter(event=self.event, slug="artist-alley-application").first()
        if survey:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug="taidekuja")
            cache = survey.universe.preload_dimensions(["location", "lipputyyppi"])
            for location in cache.values_by_dimension.get("location", {}).values():
                for ticket_type in cache.values_by_dimension.get("lipputyyppi", {}).values():
                    SurveyToBadgeMapping.objects.update_or_create(
                        survey=survey,
                        required_dimensions={
                            "location": [location.slug],
                            "lipputyyppi": [ticket_type.slug],
                        },
                        defaults=dict(
                            personnel_class=personnel_class,
                            job_title=location.title_fi,
                            annotations={"tracon2025:formattedPerks": ticket_type.title_fi},
                        ),
                    )

            # fix order
            DimensionDTO.save_many(
                survey.universe,
                [
                    DimensionDTO(
                        slug="days",
                        title=dict(
                            fi="Päivät",
                            en="Days",
                        ),
                        value_ordering=ValueOrdering.MANUAL,
                        is_key_dimension=True,
                        is_multi_value=True,
                        choices=[
                            DimensionValueDTO(slug="friday", title=dict(fi="perjantai", en="Friday")),
                            DimensionValueDTO(slug="saturday", title=dict(fi="lauantai", en="Saturday")),
                            DimensionValueDTO(slug="sunday", title=dict(fi="sunnuntai", en="Sunday")),
                        ],
                    ),
                    DimensionDTO(
                        slug="table-number",
                        title=dict(
                            fi="Pöytänumero",
                            en="Table number",
                        ),
                        value_ordering=ValueOrdering.MANUAL,
                        is_key_dimension=True,
                        choices=[
                            DimensionValueDTO(
                                slug=f"{location_character}{i}",
                                color=location_color,
                                title=dict(
                                    fi=f"{location_fi}, pöytä {i}",
                                    en=f"{location_en}, table {i}",
                                ),
                            )
                            for location_character, location_color, location_fi, location_en in [
                                ("T", "SkyBlue", "Taidekuja", "Artist Alley"),
                                ("P", "SpringGreen", "Taidepolku", "Art Trail"),
                            ]
                            for i in range(1, 41)
                        ],
                    ),
                ],
            )

            splats = [
                Splat(
                    target_field="name",
                    source_fields=["artist_name1", "artist_name2", "artist_name3"],
                    required=True,
                ),
                Splat(
                    target_field="website",
                    source_fields=["artist_site1", "artist_site2", "artist_site3"],
                    required=False,
                ),
                Splat(
                    target_field="avatar",
                    source_fields=["fixed_artist_avatar1", "fixed_artist_avatar2", "fixed_artist_avatar3"],
                    required=False,
                ),
            ]

            projection, _created = Projection.objects.update_or_create(
                scope=survey.scope,
                slug="artist-alley",
                defaults=dict(
                    is_public=True,
                    # cache_seconds=0 if settings.DEBUG else 300,
                    default_language_code="fi",
                    splats=[splat.model_dump(mode="json", by_alias=True) for splat in splats],
                    required_dimensions=dict(status=["accepted"]),
                    filterable_dimensions=["days", "location"],
                    projected_dimensions=dict(
                        tableNumber="table-number",
                        days="days",
                        location="location",
                    ),
                    order_by=["tableNumber", "name"],
                ),
            )

            projection.surveys.set([survey])

    def setup_tickets_v2(self):
        if self.dev_tickets:
            logger.warning("--dev-tickets mode active! Tickets have zero price and no payment provider is configured.")

        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Traconin lipunmyynti <liput@tracon.fi>",
                provider_id=PaymentProvider.NONE if self.dev_tickets else PaymentProvider.PAYTRAIL.value,
                terms_and_conditions_url_en="https://tracon.fi/terms-of-use-for-tracons-ticket-shop/",
                terms_and_conditions_url_fi="https://tracon.fi/lippukaupan-kayttoehdot/",
            ),
        )

        meta.ensure_partitions()

        if Quota.objects.filter(event=self.event).exists():
            return

        friday_quota, created = Quota.objects.get_or_create(
            event=self.event,
            name="Perjantai",
        )
        if created:
            friday_quota.set_quota(5500)

        saturday_quota, created = Quota.objects.get_or_create(
            event=self.event,
            name="Lauantai",
        )
        if created:
            saturday_quota.set_quota(5500)

        sunday_quota, created = Quota.objects.get_or_create(
            event=self.event,
            name="Sunnuntai",
        )
        if created:
            sunday_quota.set_quota(5500)

        if self.test or self.dev_tickets:
            available_from = now()
            available_until = now() + timedelta(days=1)
        else:
            available_from = None
            available_until = None

        friday_quota.products.get_or_create(
            event=self.event,
            title="Tracon (2025) - Perjantailippu",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("25.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        saturday_quota.products.get_or_create(
            event=self.event,
            title="Tracon (2025) - Lauantailippu",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("40.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        sunday_quota.products.get_or_create(
            event=self.event,
            title="Tracon (2025) - Sunnuntailippu",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("35.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )

        weekend_ticket, created = Product.objects.get_or_create(
            event=self.event,
            title="Tracon (2025) - Viikonloppulippu",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("50.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        if created:
            weekend_ticket.quotas.set([friday_quota, saturday_quota, sunday_quota])


class Command(BaseCommand):
    args = ""
    help = "Setup tracon2025 specific stuff"

    def add_arguments(self, parser):
        parser.add_argument("--dev-tickets", action="store_true", default=False)

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG, dev_tickets=opts["dev_tickets"])
