import logging
import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.badges.models import BadgesEventMeta
from kompassi.core.models import Event, Organization, Person, Venue
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.intra.models import IntraEventMeta, Team
from kompassi.involvement.models.involvement_to_badge import InvolvementToBadgeMapping
from kompassi.involvement.models.involvement_to_group import InvolvementToGroupMapping
from kompassi.involvement.models.meta import InvolvementEventMeta
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models import AlternativeSignupForm, JobCategory, LabourEventMeta, PersonnelClass
from kompassi.labour.models.qualifications import Qualification
from kompassi.program_v2.models.meta import ProgramV2EventMeta
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider
from kompassi.zombies.enrollment.models import SpecialDiet

from ...models import SignupExtra, WorkDay

logger = logging.getLogger(__name__)


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


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
        self.setup_program_v2()
        self.setup_badges()
        self.setup_intra()
        self.setup_tickets_v2()
        self.setup_forms()

    def setup_core(self):
        self.venue, _ = Venue.objects.get_or_create(
            name="SeAMK Frami F",
            defaults=dict(
                name_inessive="SeAMK Frami F:llä",
            ),
        )
        self.organization, _ = Organization.objects.get_or_create(
            slug="cosmocon-ry",
            defaults=dict(
                name="Cosmocon ry",
                homepage_url="https://cosmocon.fi/",
            ),
        )
        self.event, _ = Event.objects.get_or_create(
            slug="cosmocon2027",
            defaults=dict(
                name="Cosmocon 2027",
                name_genitive="Cosmoconin",
                name_illative="Cosmoconiin",
                name_inessive="Cosmoconissa",
                homepage_url="https://cosmocon.fi",
                organization=self.organization,
                start_time=datetime(2027, 2, 20, 11, 0, tzinfo=self.tz),
                end_time=datetime(2027, 2, 21, 17, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, _ = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            # Rakennus alkaa perjantai-iltapäivällä, purku päättyy sunnuntai-iltana.
            work_begins=datetime(2027, 2, 19, 12, 0, tzinfo=self.tz),
            work_ends=datetime(2027, 2, 21, 21, 0, tzinfo=self.tz),
            registration_opens=datetime(2026, 10, 26, 0, 0, tzinfo=self.tz),
            registration_closes=self.event.start_time,
            admin_group=labour_admin_group,
            contact_email="Cosmoconin vapaaehtoisvastaava <talkoo@cosmocon.fi>",
            signup_message=(
                "Cosmoconin vapaaehtoistoiminnan ikäraja on K15. Huomaathan, että osa tehtävistä "
                "vaatii korkeamman ikärajan: järjestyksenvalvonta on K18."
            ),
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )

        labour_event_meta, _ = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ("Conitea", "conitea", "labour"),
            ("Vapaaehtoinen", "vapaaehtoinen", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "program_v2"),
            ("Vieras", "vieras", "badges"),
        ]:
            PersonnelClass.objects.update_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        conitea = PersonnelClass.objects.get(event=self.event, slug="conitea")
        vapaaehtoinen = PersonnelClass.objects.get(event=self.event, slug="vapaaehtoinen")

        for jc_slug, jc_name, jc_description, jc_personnel_classes in [
            (
                "conitea",
                "Conitea",
                "Tapahtuman suunnittelusta ja valmistelusta vastaavan järjestelytoimikunnan eli conitean jäsen.",
                [conitea],
            ),
            (
                "lipunmyynti",
                "Lipunmyynti ja lipuntarkastus",
                (
                    "Vapaaehtoistehtäviin sisältyy tapahtuman pääsylippujen tarkastusta ja vaihtamista "
                    "rannekkeiksi. Tehtäviin saattaa kuulua myös lipunmyyntiä. Mikäli tapahtumaan myydään "
                    "vielä lippuja ovelta, myynti tapahtuu sekä käteismyynnillä että korttimaksulla. "
                    "Maksupääte on mallia SumUp, joka vaatii toimiakseen bluetooth-yhteyden ja sovelluksen, "
                    "joka olisi syytä löytyä ainakin yhdeltä työntekijältä jokaisessa työvuorossa. "
                    "Maksupäätteen käyttö opetetaan ennen vuoron alkua."
                ),
                [vapaaehtoinen],
            ),
            (
                "kiinteisto",
                "Kiinteistö ja viihtyvyys",
                (
                    "Vapaaehtoistehtäviin sisältyy Frami F:n infrasta sekä kävijöiden viihtyvyydestä "
                    "huolehtiminen. Huolehdit siitä, että kylmää juomavettä on saatavilla, wc-tiloissa "
                    "riittää käsi- ja wc-paperia, roskat päätyvät roskiin ja roska-astiat eivät pääse "
                    "täyttymään yli. Avustat ja toimit myös muun tuotantoryhmän silminä ja korvina "
                    "kävijöiden keskuudessa ja kerrot mahdollisista epäkohdista vastuualueen vastaavalle "
                    "tai järjestyksenvalvojalle."
                ),
                [vapaaehtoinen],
            ),
            (
                "rakennus-ja-purku",
                "Rakennus ja purku",
                (
                    "Tapahtuman rakennuksessa ja purussa autat laittamaan paikkoja järjestykseen esimerkiksi "
                    "tavaroita roudaamalla, koristelemalla ja muulla tarvittavalla! Tehtävässä vaaditaan "
                    "fyysistä jaksamista sekä mahdollisesti tuolille kiipeämistä, mutta mikään akrobaatti "
                    "tai painonnostaja ei tarvitse olla. Tapahtuman rakennus sijoittuu joko "
                    "perjantai-iltapäivälle tai lauantaiaamulle, ja tapahtuman purku ajoittuu "
                    "sunnuntai-illalle. Mikäli vapaaehtoinen osallistuu rakennukseen perjantaina tai purkuun "
                    "sunnuntaina, saa hän palkkioksi viikonlopun rannekkeen tapahtumaan eikä tarvitse tehdä "
                    "muita vapaaehtoistehtäviä tapahtuman aikana."
                ),
                [vapaaehtoinen],
            ),
            (
                "cosplay-kisa",
                "Cosplay-kisa",
                (
                    "Vapaaehtoistehtäviin sisältyy cosplay-kisavastaavan avustamista, kuten kilpailun "
                    "aikatauluista huolehtimista, kisaajien ohjeistusta paikan päällä ja tuomarien "
                    "avustamista. Teatteri- ja/tai pukuiluharrastuksesta on tässä tehtävässä etua! Sinua ei "
                    "myöskään tiukan paikan tullen pelota tarttua kuumaliimapyssyyn tai muuhun vastaavaan "
                    "työvälineeseen. Cosplay-kisan vapaaehtoiset työskentelevät koko tapahtuman ajan samassa "
                    "pestissä, ja vuoro kestää noin 7–8 tuntia."
                ),
                [vapaaehtoinen],
            ),
            (
                "myyntisali",
                "Myyntisali ja taidekuja",
                (
                    "Vapaaehtoistehtäviin sisältyy avustamista sponsori- ja myyntipöytien kanssa ennen "
                    "tapahtumaa ja sen aikana (pöytien siirtelyt, kyltittämiset, sähköjen vetäminen paikalle "
                    "jne.), myyjien tauottamista (myyntipaikan vahtimista wc- ja ruokataukojen aikana), sekä "
                    "muita avustavia työtehtäviä. Autat vastaavaa henkilöä pitämään huolen siitä, että "
                    "tapahtumaan saapuvilla myyjillä ja sponsoreilla on kaikki hyvin ja tarjoat matalalla "
                    "kynnyksellä apua, oli kyse sitten kahvin noutamisesta tai jostain isommasta."
                ),
                [vapaaehtoinen],
            ),
            (
                "jarjestyksenvalvonta",
                "Järjestyksenvalvonta",
                (
                    "Vapaaehtoistehtäviin kuuluu kävijöiden ja sidosryhmäläisten viihtyvyydestä ja "
                    "turvallisuudesta, sekä SeAMKin tilojen asianmukaisesta käytöstä huolehtiminen. "
                    "Työtehtävässä vaaditaan joko voimassaoleva JV-kortti, tai poliisilta saatava tilapäinen "
                    "lupa järjestyksenvalvojana toimimiseen. Katsomme myös eduksi, mikäli sinulta löytyy "
                    "EA-kortti tai hätäensiapukoulutus."
                ),
                [vapaaehtoinen],
            ),
            (
                "tehotiimi",
                "Tehotiimi",
                (
                    "Tehotiimin tehtävänä on olla valmiudessa auttamaan yllättävissä asioissa, tai silloin "
                    "kun jokin toinen conin työryhmä tarvitsee lisäkäsiä! Tässä tehtävässä pääasiassa "
                    "avustetaan myös vapaaehtoisvastaavaa, joka häärää conipäivän aikana myös yleisesti "
                    "muita vastaavia avustamassa sekä ohjaa tapahtuman muita vapaaehtoisia."
                ),
                [vapaaehtoinen],
            ),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=jc_slug,
                defaults=dict(
                    name=jc_name,
                    description=jc_description,
                ),
            )

            if created:
                job_category.personnel_classes.set(jc_personnel_classes)

        # Coniteaan ei haeta julkisen vapaaehtoishaun kautta, vaan omalla lomakkeellaan.
        JobCategory.objects.filter(event=self.event, slug="conitea").update(public=False)

        for jc_slug, qualification_name in [
            ("jarjestyksenvalvonta", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, slug=jc_slug)
            qual = Qualification.objects.get(name=qualification_name)
            jc.required_qualifications.set([qual])

        for work_day_name in [
            "Perjantai 19.2. (vain rakennus)",
            "Lauantai 20.2.",
            "Sunnuntai 21.2.",
        ]:
            WorkDay.objects.get_or_create(name=work_day_name)

        # SpecialDiet on jaettu kaikkien sitä käyttävien tapahtumien kesken, joten get_or_create
        # nimen perusteella käyttää olemassa olevat rivit uudelleen eikä luo duplikaatteja.
        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        labour_event_meta.create_groups()

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.cosmocon2027.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.cosmocon2027.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
                signup_message=(
                    "Täytä tämä lomake vain, jos kuulut Cosmoconin coniteaan. "
                    "Vapaaehtoiseksi haetaan tapahtuman vapaaehtoishaun kautta."
                ),
            ),
        )

    def setup_program_v2(self):
        InvolvementEventMeta.ensure(self.event)

        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])

        registry = Registry.objects.get(
            scope=self.organization.scope,
            slug="volunteers",
        )

        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                default_registry=registry,
                contact_email="Cosmoconin ohjelmavastaava <ohjelma@cosmocon.fi>",
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

    def setup_badges(self):
        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=False,
                registry=Registry.objects.get(
                    scope=self.organization.scope,
                    slug="volunteers",
                ),
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

        # Conitean vastuualueet. Tiimi ei itsessään myönnä oikeuksia Kompassissa – ne annetaan
        # erikseen intran Oikeudet-näkymästä. Tiimin auth.Group on kuitenkin se, johon
        # mahdolliset postituslistat ja GroupPrivilege-myönnöt voi jatkossa kiinnittää.
        for team_slug, team_name in [
            ("johto", "Johtoryhmä"),
            ("talous", "Talous"),
            ("viestinta", "Viestintä"),
            ("ohjelma", "Ohjelma"),
            ("cosplay", "Cosplay-kisa"),
            ("myyntisali", "Myyntisali ja taidekuja"),
            ("lipunmyynti", "Lipunmyynti"),
            ("vapaaehtoiset", "Vapaaehtoiset"),
            ("kiinteisto", "Kiinteistö ja viihtyvyys"),
            ("turva", "Turvallisuus"),
            ("tekniikka", "Tekniikka"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])

            Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                ),
            )

    def setup_tickets_v2(self):
        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Cosmocon 2027 <info@cosmocon.fi>",
                provider=PaymentProvider.PAYTRAIL,
                terms_and_conditions_url_fi="https://cosmocon.fi/info/toimitusehdot/",
            ),
        )
        meta.ensure_partitions()

    def setup_forms(self):
        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])
        FormsEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup cosmocon2027 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
