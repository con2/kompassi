from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now


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

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

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
            slug="shumicon2023",
            defaults=dict(
                public=True,
                name="Shumicon 2023",
                name_genitive="Shumiconin",
                name_illative="Shumiconiin",
                name_inessive="Shumiconissa",
                homepage_url="https://shumicon.fi",
                organization=self.organization,
                start_time=datetime(2023, 10, 21, 10, 0, tzinfo=self.tz),
                end_time=datetime(2023, 10, 22, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.utils import slugify
        from kompassi.labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )

        from ...models import KnownLanguage, NativeLanguage, SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
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
        for jc_data in [
            ("vastaava", "Vastaava", "Tapahtuman järjestelytoimikunnan jäsen", [vastaava]),
            (
                "cosplay",
                "Cosplayvänkäri",
                "Cosplayvänkäri työskentelee tapahtumassa backstagella cosplaykisojen parissa. Työtehtäviin kuuluu mm. cosplaykisaajien avustaminen sekä ohjeistus, tuomarointien aikataulujen seuraaminen ja backstagen yleisestä viihtyvyydestä huolehtiminen. HUOM! Työvuoro sijoittuu täysin lauantaipäivälle.",
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
                "Greenroomissa pidät huolta työvoimalle tarkoitetuista tarjoiluista, täydennät niitä tarpeen mukaan ja huolehdit, ettei mitään puutu. Pidät myös huolen, että greenissä on mahdollisimman siistiä. HUOM! Työtehtävä vaatii hygieniapassin.",
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
                "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä. HUOM! Hakijan täytyy olla 18-vuotias ja osata suomen lisäksi vähintään englantia.",
                [tyovoima],
            ),
            (
                "jv",
                "Järjestyksenvalvonta",
                "Järjestyksenvalvojat pitävät huolen kävijöiden turvallisuudesta tapahtuman aikana. Tehtävä edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
                [tyovoima],
            ),
            (
                "karaoke",
                "Karaoke",
                "Kun mieli tahtoo laulaa, on mentävä karaokeen. Tässä tehtävässä et niinkään pääse itse laulamaan vaan hoidat karaokepistettä muiden iloksi",
                [tyovoima],
            ),
            (
                "rannekkeenvaihto",
                "Lipunmyynti- ja vaihto",
                "Etukäteen ostettujen lippujen tarkistaminen ja vaihtaminen rannekkeisiin. Rahaa käsiteltäessä vaaditaan 18 vuoden ikää.",
                [tyovoima],
            ),
            (
                "narikka",
                "Narikka",
                "Syksyllä on jo pimeää ja kylmää, joten ihmisillä on takit päällä. Tapahtuman ajaksi ne kannattaa jättää narikkaan säilöön.",
                [tyovoima],
            ),
            (
                "ohjelmajuoksija",
                "Ohjelmajuoksija",
                "Ohjelmavänkärit tekevät tarkistuskierroksia ohjelmapisteissä ympäri tapahtumapaikkaa ja avustavat ohjelmanjärjestäjiä esim. salitekniikan käynnistämisessä. Aikaisemmasta tekniikkatietämyksestä on hyötyä tehtävässä.",
                [tyovoima],
            ),
            (
                "siivous",
                "Siivous",
                "Siivous huolehtii tapahtuma-alueen viihtyisyydestä ja huollosta: tyhjennät roska-astioita ja keräät irtoroskia tapahtuma-alueelta, sekä tarvittaessa täytät vesipisteitä.",
                [tyovoima],
            ),
            (
                "taidekuja",
                "Taidekuja",
                "Taidekujan vänkärit tekevät säännöllisesti tarkastuskäyntejä taidekujalle esim. jonotusruuhkien välttämiseksi. Lisäksi he pitävät huolta taidekujalaisista ja tarvittaessa tauottavat näitä.",
                [tyovoima],
            ),
            (
                "valokuvaus",
                "Valokuvaus",
                "Valokuvaajat ottavat kuvia tapahtumapaikalla kävijöistä, ohjelmista sekä muista mielenkiintoisista jutuista! Huom. kuvaaja sitoutuu editoimaan kuvia myös tapahtuman aikana.",
                [tyovoima],
            ),
            (
                "yleinen",
                "Yleisvänkäri",
                "Olet conissa niinsanottu joka puun höylä, eli tarvittaessa olet kutsuttavissa auttamaan muita tiimejä erilaisissa tehtävissä, kuten mm. vesipisteiden täytössä tai ruuhka-ajan narikassa.",
                [tyovoima],
            ),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                slug = slugify(name)
            elif len(jc_data) == 4:
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
                signup_form_class_path="events.shumicon2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.shumicon2023.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            reference_number_template="2023{:06d}",
            contact_email="Shumicon 2023 -lipunmyynti <lipunmyynti@shumicon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Shumicon 2023 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
            "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
            "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
            "lipunvaihtopisteessä.\n\n"
            "Jos tapahtuma joudutaan perumaan, lippusi käy sellaisenaan seuraavassa Shumiconissa tai voit saada\n"
            "hyvityksen ottamalla yhteyttä: lipunmyynti@shumicon.fi.\n\n"
            "Tervetuloa Shumiconiin!\n\n"
            "---\n\n"
            "This is your electronic ticket to Shumicon 2023. The electronic ticket will be exchanged to a wrist band\n"
            "at a ticket exchange desk on your arrival at the event. You can print this ticket or show it from the\n"
            "screen of a smartphone or tablet. If neither is possible, please write down the four or five words from\n"
            "beneath the bar code and show that at a ticket exchange desk.\n\n"
            "In case the event has to be canceled your ticket will be valid for the next Shumicon or you can be\n"
            "reimbursed for your ticket. For event cancellation related reimbursement please contact us at\n"
            "lipunmyynti@shumicon.fi.\n\n"
            "Welcome to Shumicon!",
            front_page_text="<h2>Tervetuloa Shumiconin lippukauppaan! / Welcome to Shumicon's Ticket Store!</h2>"
            "<p>Liput maksetaan oston yhteydessä Paytrailin kautta. Lippujen ostaminen vaatii suomalaiset verkkopankkitunnukset, luottokortin (Visa/Mastercard/American Express) tai MobilePayn. Pyydämme suosimaan maksamista verkkopankilla, mikäli mahdollista.</p>"
            "<p>Maksetut liput toimitetaan e-lippuina sähköpostitse asiakkaan antamaan osoitteeseen. E-liput vaihdetaan rannekkeiksi tapahtumaan saavuttaessa.</p>"
            "<p>Lisätietoja lipuista saat tapahtuman verkkosivuilta. <a href='https://shumicon.fi/lipunmyynti/'>Siirry takaisin tapahtuman verkkosivuille</a>.</p>"
            "<p>---</p>"
            "<p>The tickets are paid for at the moment of purchase via Paytrail. Purchasing a ticket requires a Finnish online banking service account, a credit card (Visa/Mastercard/American Express) or MobilePay. Paying via online banking is the most preferred option, if possible.</p>"
            "<p>Paid tickets will be sent as e-tickets to the e-mail address provided by the customer. E-tickets will be exchanged to wristbands at the event venue.</p>"
            "<p>More information about the tickets can be found on event website. <a href='https://shumicon.fi/lipunmyynti/'> Go back to the event's website</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for product_info in [
            dict(
                name="Shumicon 2023 viikonloppulippu / Weekend Ticket",
                description="Sisältää pääsyn Shumicon 2023 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Shumicon 2023 for the weekend.",
                limit_groups=[
                    limit_group("Pääsyliput", 600),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

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
        from kompassi.core.utils import full_hours_between
        from kompassi.labour.models import PersonnelClass
        from kompassi.zombies.programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            Tag,
            TimeBlock,
        )

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
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
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
            ("K-18", "label-danger"),
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
                title="Tarjoa puhe- tai muuta ohjelmaa",
                short_description="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole pöytäroolipeli.",
                programme_form_code="events.shumicon2023.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.shumicon2023.forms:ProgrammeForm"
            default_form.save()

        self.event.programme_event_meta.create_groups()

    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta, Team

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

    def handle(self, *args, **opts):
        self.setup_core()


class Command(BaseCommand):
    args = ""
    help = "Setup shumicon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
