import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now


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
        self.setup_intra()
        self.setup_tickets()
        self.setup_badges()
        self.setup_access()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Messukeskus",
            defaults=dict(
                name_inessive="Messukeskuksessa",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="http://www.ropecon.fi/hallitus",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="ropecon2025",
            defaults=dict(
                name="Ropecon 2025",
                name_genitive="Ropecon 2025 -tapahtuman",
                name_illative="Ropecon 2025 -tapahtumaan",
                name_inessive="Ropecon 2025 -tapahtumassa",
                homepage_url="http://ropecon.fi",
                organization=self.organization,
                start_time=datetime(2025, 7, 25, 15, 0, tzinfo=self.tz),
                end_time=datetime(2025, 7, 27, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Event, Person
        from labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
        )

        from ...models import Language, SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=(self.event.start_time - timedelta(days=2)).replace(hour=8, minute=0, tzinfo=self.tz),  # type: ignore
            work_ends=self.event.end_time.replace(hour=23, minute=0, tzinfo=self.tz),  # type: ignore
            admin_group=labour_admin_group,
            contact_email="Ropecon 2025 vapaaehtoisvastaava <vapaaehtoiset@ropecon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ("Conitea", "conitea", "labour"),
            ("Vuorovastaava", "ylivankari", "labour"),
            ("Ylityöntekijä", "ylityovoima", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "program_v2"),
            ("Guest of Honour", "goh", "program_v2"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Vieras", "vieras", "badges"),
            ("Vapaalippu", "vapaalippu", "badges"),
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

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="ropecon2023"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for language in [
            "suomi / Finnish",
            "englanti / English",
            "ruotsi / Swedish",
            "saksa / German",
            "japani / Japanese",
            "eesti / Estonian",
        ]:
            Language.objects.get_or_create(name=language)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.ropecon2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.ropecon2025.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="xxlomake",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.ropecon2025.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.ropecon2025.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Ropeconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella."
                ),
            ),
        )

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            tickets_view_version="v1.5",
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            reference_number_template="2025{:06d}",
            contact_email="Ropecon 2025 -lipunmyynti <lipunmyynti@ropecon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Ropecon 2025 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Ranneke tulee pitää ranteessa koko lipun\n"
            "voimassaoloajan. Voit tulostaa tämän lipun tai näyttää sen älypuhelimen tai tablettitietokoneen näytöltä.\n"
            "Mikäli kumpikaan näistä ei ole mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä\n"
            "sanasta koostuva Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Jos tapahtuma joudutaan perumaan, voit saada hyvityksen ottamalla yhteyttä: lipunmyynti@ropecon.fi. \n\n"
            "Tervetuloa Ropeconiin!\n\n"
            "---\n\n"
            "This is your electronic ticket to Ropecon 2025. The electronic ticket will be exchanged to a wrist band\n"
            "at a ticket exchange desk on your arrival at the event. The wristband must be kept on the wrist for\n"
            "the entire duration of the ticket validity. You can print this ticket or show it from the screen of\n"
            "a smartphone or tablet. If neither is possible, please write down the four or five words from\n"
            "beneath the bar code and show that at a ticket exchange desk.\n\n"
            "In case the event has to be canceled you can be reimbursed for your ticket.\n"
            "For event cancellation related reimbursement please contact us at lipunmyynti@ropecon.fi.\n\n"
            "Welcome to Ropecon!",
            front_page_text="<h2>Tervetuloa Ropeconin lippukauppaan! / Welcome to Ropecon's Ticket Store!</h2>"
            "<p>Liput maksetaan oston yhteydessä Paytrailin kautta. Lippujen ostamiseen tarvitset suomalaiset verkkopankkitunnukset, luottokortin (Visa/Mastercard/American Express) tai MobilePayn. Pyydämme suosimaan verkkopankkia, mikäli mahdollista.</p>"
            "<p>Maksetut liput toimitetaan e-lippuina sähköpostitse asiakkaan antamaan osoitteeseen. E-liput vaihdetaan rannekkeiksi tapahtumaan saavuttaessa. Ranneke tulee pitää ranteessa koko lipun voimassaoloajan.</p>"
            "<p>Lisätietoja lipuista saat tapahtuman verkkosivuilta. <a href='https://ropecon.fi/liput/lippuehdot/' target='_blank'>Luethan päivitetyt lippuehdot verkkosivuilta</a>.</p>"
            "<p>---</p>"
            "<p>The tickets must be paid at purchase using a Finnish online banking service, credit card (Visa/Mastercard/American Express) or MobilePay. We would prefer payment through online banking, if possible.</p>"
            "<p>Paid tickets will be sent as e-tickets to the e-mail address provided by the costumer. E-tickets will be exchanged to wrist bands at the event venue. The wristband must be kept on the wrist for the entire duration of the ticket validity.</p>"
            "<p>More information about the tickets can be found on Ropecon's website. <a href='https://ropecon.fi/en/tickets/terms-and-conditions/' target='_blank'>Please read updated ticket terms and contions</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),  # type: ignore
                ticket_sales_ends=t + timedelta(days=60),  # type: ignore
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
            # dict(
            #     name="Ropecon 2025 Early Dragon viikonloppu / Weekend Ticket",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for the weekend.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=4000,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 lasten Early Dragon viikonloppu / Children's Weekend Ticket",
            #     description="Sisältää pääsyn lapselle (7-12v) Ropecon 2025 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for children (aged 7-12) for the weekend.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=2000,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Early Dragon perhelippu (vkl) / Family Ticket (wknd)",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan 2 aikuiselle ja 1 - 3 lapselle (7-12 v) koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for two adults and 1-3 children (aged 7-12) for the weekend",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=9900,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 viikonloppu / Weekend Ticket",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for the weekend.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=4500,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 lasten viikonloppu / Children's Weekend Ticket",
            #     description="Sisältää pääsyn lapselle (7-12v) Ropecon 2025 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for children (aged 7-12) for the weekend.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=2500,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 perhelippu (vkl) / Family Ticket (wknd)",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan 2 aikuiselle ja 1 - 3 lapselle (7-12 v) koko viikonlopun ajan. / Includes the entrance to Ropecon 2025 for two adults and 1-3 children (aged 7-12) for the weekend",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=11000,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Academic Seminar and Friday Ticket",
            #     description="Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2025 -tapahtumaan perjantaina. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar and Ropecon 2025 on friday. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target='_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=5500,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Academic Seminar and Weekend Ticket",
            #     description="Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2025 -tapahtumaan koko viikonlopun ajan. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar and Ropecon 2025 for the weekend. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=6600,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Academic seminar",
            #     description="Sisältää pääsyn Akateemiseen seminaariin. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=2100,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Perjantai aikuinen / Friday Ticket ",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan perjantain ajan. / Includes the entrance to Ropecon 2025 for the Friday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=3400,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Lauantai aikuinen / Saturday Ticket",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan lauantain ajan. / Includes the entrance to Ropecon 2025 for the Saturday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=3400,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Sunnuntai aikuinen / Sunday Ticket",
            #     description="Sisältää pääsyn Ropecon 2025 -tapahtumaan sunnuntain ajan. / Includes the entrance to Ropecon 2025 for the Sunday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=2000,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Perjantai lapsi / Children's Friday Ticket",
            #     description="Sisältää pääsyn lapselle (7-12v) Ropecon 2025 -tapahtumaan perjantain ajan. / Includes the entrance to Ropecon 2025 for children (aged 7-12) for the Friday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=1500,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Lauantai lapsi / Children's Saturday Ticket",
            #     description="Sisältää pääsyn lapselle (7-12v) Ropecon 2025 -tapahtumaan lauantain ajan. / Includes the entrance to Ropecon 2025 for children (aged 7-12) for the Saturday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=1500,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Sunnuntai lapsi / Children's Sunday Ticket",
            #     description="Sisältää pääsyn lapselle (7-12v) Ropecon 2025 -tapahtumaan sunnuntain ajan. / Includes the entrance to Ropecon 2025 for children (aged 7-12) for the Sunday.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=1000,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Ropecon 2025 Haltiakummilippu / Fairy Godparent Ticket",
            #     description="Lahjoittaa viikonloppupääsyn Haltiakummilippua hakevalle Ropecon 2025 -tapahtumaan. HUOM: Tämä lahjoitustuote ei sisällä sisäänpääsyä itsellesi. / Buy this product to donate a ticket to someone who applies for a Godparent ticket. NOTE: This product does not include admission for yourself.",
            #     limit_groups=[
            #         limit_group("Pääsyliput", 9999),
            #     ],
            #     price_cents=4000,
            #     electronic_ticket=False,
            #     available=False,
            #     ordering=self.get_ordering_number(),
            #     mail_description="\n".join(
            #         line.strip()
            #         for line in """
            #             Kiitämme osallistumisestasi Haltiakummilippukeräykseen! <3
            #             Haltiakummiliput jaetaan hakijoiden kesken heinäkuussa.
            #             Thank you for participating in collection of Fairy Godparent tickets! <3
            #             The tickets will be distributed among participants in July.
            #         """.strip().splitlines()
            #     ),
            # ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
                product.save()

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
            ),
        )

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("conitea")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("talous", "Talous"),
            ("peliohjelma", "Peliohjelma"),
            ("ohjelma", "Puhe- ja muu ohjelma"),
            ("viestinta", "Viestintä"),
            ("tilat", "Tilat"),
            ("tekniikka", "Tekniikka"),
            ("vapaaehtoiset", "Vapaaehtoiset"),
            ("kavijapalvelut", "Kävijäpalvelut"),
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

    def setup_access(self):
        from access.models import EmailAliasType, GroupEmailAliasGrant

        cc_group = self.event.labour_event_meta.get_group("conitea")

        for metavar in [
            "firstname.lastname",
            "nick",
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name="ropecon.fi", metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                ),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup ropecon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
