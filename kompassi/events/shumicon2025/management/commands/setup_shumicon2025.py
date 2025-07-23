from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.models import Event, Organization, Venue
from kompassi.core.utils import full_hours_between
from kompassi.intra.models import IntraEventMeta, Team
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
    Qualification,
)
from kompassi.program_v2.models.meta import ProgramV2EventMeta
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider
from kompassi.zombies.programme.models import (
    AlternativeProgrammeForm,
    Category,
    ProgrammeEventMeta,
    Role,
    SpecialStartTime,
    Tag,
    TimeBlock,
)

from ...models import KnownLanguage, NativeLanguage, SignupExtra, SpecialDiet


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
        # self.setup_tickets()
        # self.setup_programme()
        self.setup_intra()
        # self.setup_access()
        # self.setup_kaatoilmo()
        # self.setup_sms()
        self.setup_program_v2()
        self.setup_tickets_v2()

    def setup_core(self):
        self.organization, unused = Organization.objects.get_or_create(
            slug="paakaupunkiseudun-cosplay-ry",
            defaults=dict(
                name="Pääkaupunkiseudun Cosplay ry",
                homepage_url="https://pkscosplay.wordpress.com/",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(
            name="Kulttuurikeskus Stoa",
            defaults=dict(
                name_inessive="Kulttuurikeskus Stoassa",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="shumicon2025",
            defaults=dict(
                public=True,
                name="Shumicon 2025",
                name_genitive="Shumiconin",
                name_illative="Shumiconiin",
                name_inessive="Shumiconissa",
                homepage_url="https://shumicon.fi",
                organization=self.organization,
                start_time=datetime(2025, 5, 24, 10, 0, tzinfo=self.tz),
                end_time=datetime(2025, 5, 25, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2025, 5, 23, 10, 0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),  # type: ignore
            admin_group=labour_admin_group,
            contact_email="Shumicon <tyovoima@shumicon.fi>",
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

        for pc_prio, pc_name, pc_slug, pc_app_label in [
            (10, "Vastaavat", "vastaava", "labour"),
            (20, "Työvoima", "tyovoima", "labour"),
            (30, "Ohjelmanjärjestäjä", "ohjelma", "programme"),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=pc_prio,
                ),
            )

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        # if not JobCategory.objects.filter(event=self.event).exists():
        for slug, name, description, pcs in [
            ("vastaava", "Vastaava", "Tapahtuman järjestelytoimikunnan jäsen", [vastaava]),
            (
                "cosplay",
                "Cosplayvänkäri",
                "Cosplaytirpat työskentelevät Shumiconin monien cosplaykilpailujen parissa kulissien takana. Työtehtäviin kuuluu mm. cosplaykilpailijoiden avustaminen sekä ohjeistus, tuomarointien aikataulujen seuraaminen, sekä backstagen yleisestä viihtyvyydestä huolehtiminen. Työvuoro sijoittuu yleensä kokonaan lauantaipäivälle, sillä sunnuntaina ei ole cosplaykilpailuja.",
                [tyovoima],
            ),
            (
                "erikoinen",
                "Erikoistehtävä",
                "Haethan erikoistehtävää vain, jos sinulle on erikseen näin ohjeistettu. Selvennäthän vapaatekstikenttään lopussa, mikä on hakemasi tehtävä.",
                [tyovoima],
            ),
            (
                "greenroom",
                "Greenroom",
                "Green Room on tapahtuman työvoiman ja ohjelmanpitäjien taukotila, missä voi huilia työvuorojen välissä. Green Room -tirppana pidät huolta työvoimalle tarkoitetuista tarjoiluista, täydennät niitä tarpeen mukaan ja huolehdit, ettei mitään puutu. Pidät myös huolen siitä, että taukotilassa on mahdollisimman siistiä.Työtehtävä vaatii hygieniapassin. Hygieniapassi on todistus, jonka myöntää Ruokavirasto.",
                [tyovoima],
            ),
            (
                "hairintayhdyshenkilo",
                "Häirintäyhdyshenkilö",
                "Häirintäyhdyshenkilöt ovat kävijöiden tavoitettavissa koko tapahtuman ajan ja auttavat ratkaisemaan mahdollisia häirintätilanteita. Et tarvitse tehtävään häirintäyhdyshenkilökoulutusta, mutta se katsotaan eduksi. Voit työskennellä häirintäyhdyshenkilönä muiden tehtävien ohella. Häirintäyhdyshenkilön toiminta tapahtumassa on ehdottoman luottamuksellista.",
                [tyovoima],
            ),
            (
                "info",
                "Info",
                "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä. Infopisteen tirpoilta vaaditaan 18 vuoden ikää sekä toivotaan suomen kielen lisäksi vähintään englannin kielen taitoa. Muustakin kieliosaamisesta on valtavaa hyötyä infossa työskennellessä!",
                [tyovoima],
            ),
            (
                "jv",
                "Järjestyksenvalvonta",
                "Jotta kaikilla olisi turvallinen conikokemus, tarvitsemme järjestyksenvalvojia turvallisuusvastaavan tiimiin! Järjestyksenvalvojien tehtävänä on siis kävijöiden turvallisuuden valvominen conipaikalla. Työskentely tässä tiimissä edellyttää voimassa olevaa JV-korttia sekä asiakaspalveluasennetta. Huomioithan, että et voi valita tätä tehtävää hakemuksessa, ellet ole täyttänyt Kompassi-profiiliisi JV-korttisi numeroa.",
                [tyovoima],
            ),
            (
                "rannekkeenvaihto",
                "Lipunmyynti- ja vaihto",
                "Lipunmyynnin ja -vaihdon tirpat ovat kävijöiden ensikosketus tapahtumaan. Lipunvaihdossa lipputirpat vastaanottavat kävijät ja vaihtavat näiden ostamat liput rannekkeisiin. Lipputirpat voidaan myös sijoittaa myymään tapahtuman oheistuotteita kun rannekkeenvaihto on ohi. Lipputirpan hommissa pärjää hyvällä asiakaspalveluasenteella ja pirteällä hymyllä. Rahaa käsiteltäessä vaaditaan 18 vuoden ikää.",
                [tyovoima],
            ),
            (
                "narikka",
                "Narikka",
                "Narikkatirpat pyörittävät conin narikkaa. Narikkoja voi olla useampia, esimerkiksi takkinarikka ja isotavaranarikka erikseen. Takkinarikassa voi työskennellä käytännössä kuka vain, sillä takkinarikkaan jätettävät tavarat ovat – kuten nimestä voi päätellä – yleensä takkeja tai kevyitä laukkuja ja kasseja. Narikassa seisotaan paljon ja meno voi olla todella ripeää ruuhka-aikana, joten narikkahommissa pärjää hyvin stressinsietokyvyllä ja hyvillä kengillä.",
                [tyovoima],
            ),
            (
                "ohjelmajuoksija",
                "Ohjelma ja karaoke",
                "Coneissa on yleensä monenlaista ohjelmaa, joita ohjelmanpitäjät tulevat järjestämään ohjelmanhaun kautta. Ohjelmatirppojen tehtävä on avustaa ohjelmanpitäjiä käytännön asioiden kanssa conipaikalla niin ennen heidän ohjelmanumeroaan kuin joskus sen aikanakin. Tyypillisintä on auttaa ohjelmanpitäjiä salin laitteiden kanssa, esimerkiksi kun diaesitys ei näy ruudulla tai mikrofonista ei kuulu ääni. Myös monien conikävijöiden kestosuosikki karaoke kuuluu ohjelman alle! Karaoketirppa huolehtii, että jonotus karaokeen sujuu mutkattomasti ja oikeudenmukaisesti, tarjoaa biisikatalogia uusille jonottajille ja varmistaa, että kaikki halukkaat pääsevät laulamaan.",
                [tyovoima],
            ),
            (
                "siivous",
                "Siisteys",
                "Siisteys- ja somistustiimi huolehtii tapahtuma-alueen viihtyisyydestä ja huollosta: roska-astioiden tyhjentäminen ja irtoroskien kerääminen tapahtuma-alueelta, sekä tarvittaessa vesipisteiden täyttö. Tehtäviin voi myös sisältyä mahdollisten läikkyneiden juomien tai ruokien siistiminen lattioilta sekä pintojen desinfiointi ympäri tapahtumaa. Shumiconissa osana siivoustiimin tehtäviä on myös tapahtuma-alueen somistus.",
                [tyovoima],
            ),
            (
                "taidekuja",
                "Taidekuja-apulaiset",
                "Shumiconista löytyy taidekuja sekä tietenkin myyntisali. Molemmat alueet ovat hyvin suosittuja, ja koska niihin on vapaa pääsy, niihin voi odottaa syntyvän ajoittain ruuhkaa. Silloin taidekuja-apulaiset tulevat hätään! Taidekujan tirpat tekevät säännöllisesti tarkastuskäyntejä taidekujalle ja myyntisaliin kävijäviihtyvyyden varmistamiseksi. Lisäksi he pitävät huolta taidekujalaisista ja tarvittaessa tauottavat näitä, sillä kaikilla kujalaisilla ei ole pöytäavustajaa omasta takaa.",
                [tyovoima],
            ),
            (
                "valokuvaus",
                "Valo- ja videokuvaajat",
                "Valo- ja videokuvaajat taltioivat tapahtuman ohjelmia, kävijöitä ja hetkiä tapahtumassa sekä muistoiksi paikalla olleille että markkinointimateriaaliksi tapahtumalle. Kuvaajilla tulee olla oma kamera kuvatessa sekä valmius editoida itse kuvansa tai videonsa. Muista työnkuvista poiketen kuvaajilla ei ole määriteltyjä työvuoroja, sillä odotusarvo on, että tapahtumaa kuvataan paikalla ollessa tasaisesti, mutta kuvaajat saavat muiden vapaaehtoisten tapaan toivoa vapaita hetkiä esimerkiksi käydäkseen tietyssä ohjelmassa.",
                [tyovoima],
            ),
            (
                "yleinen",
                "Yleistirpat",
                "Yleistirpat ovat todellisia monitaitureita, jotka rientävät auttamaan muissa tiimeissä ruuhkahetkinä tai kun tiimissä on vajautta vaikkapa sairastapauksen takia. Yleistirppailu on oiva tapa nähdä, mitä muissa tiimeissä loppujen lopuksi tehdään, sillä yleistirppa saattaa tapahtuman aikana käydä auttamassa jokaisessa tiimissä hetken!",
                [tyovoima],
            ),
        ]:
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

        for slug in ["vastaava"]:
            JobCategory.objects.filter(event=self.event, slug=slug).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
            ("Greenroom", "Hygieniapassi"),
        ]:
            try:
                jc = JobCategory.objects.get(event=self.event, name=jc_name)
                qual = Qualification.objects.get(name=qualification_name)
                jc.required_qualifications.set([qual])
            except JobCategory.DoesNotExist:
                pass

        for language in ["Suomi", "Ruotsi", "Englanti", "Venäjä", "Somali", "Muu, mikä?"]:
            NativeLanguage.objects.get_or_create(name=language)

        for language in [
            "Suomi",
            "Ruotsi",
            "Englanti",
            "Venäjä",
            "Somali",
            "Viittomakieli",
        ]:
            KnownLanguage.objects.get_or_create(name=language)

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                title="Vastaavien ilmoittautumislomake",
                signup_form_class_path="events.shumicon2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.shumicon2025.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

    def setup_badges(self):
        from kompassi.badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_programme(self):
        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Shumicon ohjelmatiimi <ohjelma@shumicon.fi>",
                schedule_layout="full_width",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                ),
            )

            Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=f"Näkymätön {role_title.lower()}",
                defaults=dict(
                    override_public_title=role_title,
                    is_default=False,
                    is_public=False,
                ),
            )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ("Puheohjelma", "color2"),
                ("Miitti", "miitti"),
                ("Työpaja", "color3"),
                ("One night illusion -esiintyjä", "color1"),
                ("Muu ohjelma", "muu"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),  # type: ignore
                self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),  # type: ignore
            ),
            (
                self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),  # type: ignore
                self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),  # type: ignore
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(end_time=end_time),
            )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Quarter hours
            # [:-1] – discard 18:00 to 19:00
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                # for minute in [15, 30, 45]:
                for minute in [30]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=minute),
                    )

        for tag_title, tag_class in [
            ("Suositeltu", "hilight"),
            ("Musiikki", "label-info"),
            ("In English", "label-success"),
            ("English OK", "label-success"),
            ("Paikkaliput", "label-default"),
            ("Kirkkaita/välkkyviä valoja", "label-warning"),
            ("Kovia ääniä", "label-warning"),
            ("Savutehosteita", "label-warning"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

        default_form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa ohjelmaa tai esitystä",
                short_description="Voit tarjota puheohjelmia, miittejä, työpajoja tai esitystä.",
                programme_form_code="events.shumicon2025.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.shumicon2025.forms:ProgrammeForm"
            default_form.save()

        self.event.programme_event_meta.create_groups()

    def setup_intra(self):
        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("vastaava")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("infra", "Infra"),
            ("ohjelma", "Ohjelma"),
            ("palvelut", "Palvelut"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                ),
            )

        for team in Team.objects.filter(event=self.event):
            team.is_public = team.slug != "tracoff"
            team.save()

    def setup_program_v2(self):
        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])

        # TODO(Shumicon): Define your volunteer registry
        registry, _created = Registry.objects.get_or_create(
            scope=self.organization.scope,
            slug="volunteers",
            defaults=dict(
                title_fi="Pääkaupunkiseudun Cosplay ry:n vapaaehtoisrekisteri",
                title_en="Volunteers of Pääkaupunkiseudun Cosplay ry",
            ),
        )

        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                default_registry=registry,
            ),
        )

    def setup_tickets_v2(self):
        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                provider_id=PaymentProvider.PAYTRAIL.value,
            ),
        )
        meta.ensure_partitions()


class Command(BaseCommand):
    args = ""
    help = "Setup shumicon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
