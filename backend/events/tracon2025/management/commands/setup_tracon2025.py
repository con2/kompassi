from __future__ import annotations

import logging
from datetime import datetime, timedelta
from decimal import Decimal

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils.timezone import now

from access.models import EmailAliasType, GroupEmailAliasGrant, GroupPrivilege, Privilege
from badges.emperkelators.tracon2024 import TicketType, TraconEmperkelator
from badges.models.badges_event_meta import BadgesEventMeta
from core.models.event import Event
from core.models.organization import Organization
from core.models.person import Person
from core.models.venue import Venue
from forms.models.meta import FormsEventMeta
from forms.models.survey import SurveyDTO
from intra.models import IntraEventMeta, Team
from labour.models import Survey
from labour.models.alternative_signup_forms import AlternativeSignupForm
from labour.models.info_link import InfoLink
from labour.models.job_category import JobCategory
from labour.models.labour_event_meta import LabourEventMeta
from labour.models.personnel_class import PersonnelClass
from labour.models.qualifications import Qualification
from labour.models.survey import Survey as LabourSurvey
from program_v2.importers.tracon2024 import TraconImporter
from program_v2.models.dimension_dto import Dimension, DimensionDTO
from program_v2.models.meta import ProgramV2EventMeta
from programme.models import Category, Programme, Room
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.models.product import Product
from tickets_v2.models.quota import Quota
from tickets_v2.optimized_server.models.enums import PaymentProvider

from ...models import Night, Poison, SignupExtra

logger = logging.getLogger("kompassi")


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
        self.setup_access()
        self.setup_tickets_v2()
        self.setup_forms()
        # self.setup_kaatoilmo()

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
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Traconin työvoimatiimi <tyovoima@tracon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
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
                TraconEmperkelator(
                    override_formatted_perks="Coniitin kirjekuori, valittu työvoimatuote, ekstrakangaskassi",
                ),
            ),
            (
                "Duniitti",
                "duniitti",
                "labour",
                TraconEmperkelator(ticket_type=TicketType.SUPER_INTERNAL_BADGE, meals=2, swag=True),
            ),
            (
                "Vuorovastaava",
                "vuorovastaava",
                "labour",
                TraconEmperkelator(ticket_type=TicketType.SUPER_INTERNAL_BADGE, meals=2, swag=True),
            ),
            (
                "Työvoima",
                "tyovoima",
                "labour",
                TraconEmperkelator(ticket_type=TicketType.INTERNAL_BADGE, meals=2, swag=True),
            ),
            (
                "Ohjelma",
                "ohjelma",
                "program_v2",
                TraconEmperkelator(),  # handled in programme.Role
            ),
            (
                "Guest of Honour",
                "goh",
                "programme",
                "GoH-tiimi hoitaa (ei jaeta ovelta)",
            ),
            ("Media", "media", "badges", "Badge (external)"),
            ("Myyjä", "myyja", "badges", "Myyjäranneke"),
            ("Artesaani", "artesaani", "badges", "?"),
            ("Vieras", "vieras", "badges", "Badge (external)"),
            ("Vapaalippu, viikonloppu", "vapaalippu-vkl", "tickets", "Viikonloppuranneke"),
            ("Vapaalippu, lauantai", "vapaalippu-la", "tickets", "Lauantairanneke"),
            ("Vapaalippu, sunnuntai", "vapaalippu-su", "tickets", "Sunnuntairanneke"),
            ("Cosplaykisaaja", "cosplay", "tickets", "?"),
            ("AMV-kisaaja", "amv", "tickets", "?"),
            ("Taidekuja", "taidekuja", "tickets", "?"),
            ("Taidepolku", "taidepolku", "tickets", "?"),
            ("Yhdistyspöydät", "yhdistyspoydat", "tickets", "?"),
        ]:
            if len(pc_data) == 4:
                pc_name, pc_slug, pc_app_label, pc_perks = pc_data
                perks = (
                    pc_perks
                    if isinstance(pc_perks, TraconEmperkelator)
                    else TraconEmperkelator(override_formatted_perks=pc_perks)
                )

            else:
                pc_name, pc_slug, pc_app_label = pc_data
                perks = TraconEmperkelator()

            PersonnelClass.objects.update_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                    perks=perks.model_dump(),
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
                    "Tarjoamme työvoimatuotteeksi joko juomapullon tai paidan. Valitse tässä kumpi, "
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
                emperkelator_name="tracon2024",
            ),
        )

    def setup_program_v2(self):
        try:
            room_dimension = Dimension.objects.get(universe=self.event.program_universe, slug="room")
        except Dimension.DoesNotExist:
            dimensions = TraconImporter(self.event).get_dimensions()
            dimensions = DimensionDTO.save_many(self.event, dimensions)
            room_dimension = next(d for d in dimensions if d.slug == "room")

        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                location_dimension=room_dimension,
                importer_name="tracon2025",
                admin_group=self.event.programme_event_meta.admin_group,
            ),
        )

    def setup_access(self):
        # Grant accepted workers access to Tracon Slack
        privilege = Privilege.objects.get(slug="tracon-slack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            # self.event.programme_event_meta.get_group("hosts"), # TODO program_v2 equivalent
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

        cc_group = self.event.labour_event_meta.get_group("conitea")

        for metavar in [
            "etunimi.sukunimi",
            "nick",
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name="tracon.fi", metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                ),
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

    def setup_kaatoilmo(self):
        assert self.event.start_time
        saturday = self.event.start_time + timedelta(days=1)

        coaches = []
        for coach_title, room_title, hour in [
            ("Kaatobussin paikkavaraus, menomatka", "Kaatobussi meno", 14),
            ("Kaatobussin paikkavaraus, paluumatka", "Kaatobussi paluu", 21),
        ]:
            coach, created = Programme.objects.get_or_create(
                category=Category.objects.get(title="Muu ohjelma", event=self.event),
                title=coach_title,
                defaults=dict(
                    room=Room.objects.get_or_create(event=self.event, name=room_title)[0],
                    start_time=(saturday + timedelta(days=14)).replace(hour=hour, minute=0, second=0, tzinfo=self.tz),
                    length=4 * 60,  # minutes
                    is_using_paikkala=True,
                    is_paikkala_public=False,
                    is_paikkala_time_visible=False,
                ),
            )

            coach.paikkalize(
                max_tickets_per_user=1,
                max_tickets_per_batch=1,
                reservation_start=self.event.start_time,
                numbered_seats=False,
            )

            coaches.append(coach)

        outward_coach, return_coach = coaches

        kaatoilmo_override_does_not_apply_message = (
            "Valitettavasti et pysty ilmoittautumaan kaatoon käyttäen tätä lomaketta. Tämä "
            "voi johtua siitä, että sinua ei ole kutsuttu kaatoon, tai teknisestä syystä. "
            "Kaatoon osallistumaan ovat oikeutettuja kaatopäivänä 18 vuotta täyttäneet "
            "coniitit, vuorovastaavat, vänkärit sekä badgelliset ohjelmanjärjestäjät. "
            "Mikäli saat tämän viestin siitä huolimatta, että olet mielestäsi oikeutettu "
            "osallistumaan kaatoon, ole hyvä ja ota sähköpostitse yhteyttä osoitteeseen "
            '<a href="mailto:kaatajaiset@tracon.fi">kaatajaiset@tracon.fi</a>.'
        )
        outward_coach_url = reverse("programme:paikkala_reservation_view", args=(self.event.slug, outward_coach.id))
        return_coach_url = reverse("programme:paikkala_reservation_view", args=(self.event.slug, return_coach.id))
        kaatoilmo, unused = Survey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen kaatajaisiin",
                description=(
                    "Kiitokseksi työpanoksestasi tapahtumassa Tracon tarjoaa sinulle mahdollisuuden "
                    "osallistua kaatajaisiin lauantaina 23. syyskuuta 2025 Tampereella. Kaatajaisiin osallistuminen edellyttää ilmoittautumista ja 18 vuoden ikää. "
                    "</p><p>"
                    "<strong>HUOM!</strong> Paikat kaatobusseihin varataan erikseen. Varaa paikkasi "
                    f'<a href="{outward_coach_url}" target="_blank" rel="noopener noreferrer">menobussiin täältä</a> ja '
                    f'<a href="{return_coach_url}" target="_blank" rel="noopener noreferrer">paluubussiin täältä</a>. '
                    f'Näet bussivarauksesi <a href="{reverse("programme:profile_reservations_view")}" target="_blank" rel="noopener noreferrer">paikkalippusivulta</a>.'
                ),
                override_does_not_apply_message=kaatoilmo_override_does_not_apply_message,
                form_class_path="events.tracon2025.forms:AfterpartyParticipationSurvey",
                active_from=self.event.end_time,
                active_until=datetime(2025, 9, 17, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for poison_name in [
            "Olut",
            "Siideri, kuiva",
            "Siideri, makea",
            "Lonkero",
            "Panimosima",
            "Punaviini",
            "Valkoviini",
            "Cocktailit",
            "Alkoholittomat juomat",
        ]:
            Poison.objects.get_or_create(name=poison_name)

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
                slug="kickoff-signup",
                anonymity="name_and_email",
                max_responses_per_user=1,
                login_required=True,
            ),
            SurveyDTO(
                slug="expense-claim",
                key_fields=["title", "amount"],
                login_required=True,
                anonymity="name_and_email",
            ),
            SurveyDTO(
                slug="car-usage",
                key_fields=["title", "kilometers"],
                login_required=True,
                anonymity="name_and_email",
            ),
        ]:
            survey.save(self.event)

    def setup_tickets_v2(self):
        if self.dev_tickets:
            logger.warning("--dev-tickets mode active! Tickets have zero price and no payment provider is configured.")

        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                provider_id=PaymentProvider.NONE if self.dev_tickets else PaymentProvider.PAYTRAIL.value,
            ),
        )

        meta.ensure_partitions()

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
