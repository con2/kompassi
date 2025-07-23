import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.utils import full_hours_between
from kompassi.core.utils.pkg_resources_compat import resource_string


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
        # self.setup_programme()
        # self.setup_tickets()
        self.setup_badges()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

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
            slug="ropecon2020",
            defaults=dict(
                name="Ropecon 2020",
                name_genitive="Ropecon 2020 -tapahtuman",
                name_illative="Ropecon 2020 -tapahtumaan",
                name_inessive="Ropecon 2020 -tapahtumassa",
                homepage_url="http://2020.ropecon.fi",
                organization=self.organization,
                start_time=datetime(2020, 7, 24, 15, 0, tzinfo=self.tz),
                end_time=datetime(2020, 7, 26, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Event, Person
        from kompassi.labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )

        from ...models import SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=23, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Ropecon 2020 -työvoimatiimi <tyovoima@ropecon.fi>",
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
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Guest of Honour", "goh", "programme"),
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
                source_event=Event.objects.get(slug="ropecon2019"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

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
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.ropecon2020.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.ropecon2020.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

    def setup_programme(self):
        from kompassi.labour.models import PersonnelClass
        from kompassi.zombies.programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            Tag,
            TimeBlock,
            View,
        )

        from ...models import TimeSlot

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Ropecon 2020 -ohjelmatiimi <ohjelma@ropecon.fi>",
                schedule_layout="reasonable",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        if not Room.objects.filter(event=self.event).exists():
            for room_name in [
                "Halli 3",
                "Halli 3 Bofferialue",
                "Halli 1 Myyntialue",
                "Halli 3 Näyttelyalue",
                "Halli 3 Korttipelialue",
                "Halli 3 Figupelialue",
                "Halli 3 Pukukilpailutiski",
                "Halli 3 Ohjelmalava",
                "Halli 3 Puhesali",
                "Halli 3 Ohjelmasali",
                "Ylä-Galleria",
                "Ala-Galleria",
                "Larp-tiski",
                "Messuaukio",
                "Klubiravintola",
                "Sali 103",
                "Sali 201",
                "Sali 202",
                "Sali 203a",
                "Sali 203b",
                "Sali 204",
                "Sali 205",
                "Sali 206",
                "Sali 207",
                "Sali 211",
                "Sali 212",
                "Sali 213",
                "Sali 214",
                "Sali 215",
                "Sali 216",
                "Sali 216a",
                "Sali 217",
                "Sali 218",
                "Sali 301",
                "Sali 302",
                "Sali 303",
                "Sali 304",
                "Sali 305",
                "Sali 306",
                "Sali 307",
                "Salin 203 aula",
            ]:
                room, created = Room.objects.get_or_create(
                    event=self.event,
                    name=room_name,
                )

        priority = 0
        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
            ("ohjelma", "Näkymätön ohjelmanjärjestäjä", False),
            ("ohjelma", "Peliohjelmanjärjestäjä", False),
            ("ohjelma", "Larp-pelinjohtaja", False),
            ("ohjelma", "Roolipelinjohtaja", False),
            ("ohjelma", "Ohjelmanjärjestäjä, päivälippu", False),
            ("ohjelma", "Peliohjelmanjärjestäjä, päivälippu", False),
            ("ohjelma", "Larp-pelinjohtaja, päivälippu", False),
            ("ohjelma", "Roolipelinjohtaja, päivälippu", False),
            ("ohjelma", "Ohjelmanjärjestäjä, työvoimaedut", False),
            ("ohjelma", "Peliohjelmanjärjestäjä, työvoimaedut", False),
            ("ohjelma", "Larp-pelinjohtaja, työvoimaedut", False),
            ("ohjelma", "Roolipelinjohtaja, työvoimaedut", False),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, created = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                    priority=priority,
                ),
            )

            if not created:
                role.priority = priority
                role.save()

            priority += 10

        Role.objects.get_or_create(
            personnel_class=personnel_class,
            title="Näkymätön ohjelmanjärjestäjä",
            defaults=dict(
                override_public_title="Ohjelmanjärjestäjä",
                is_default=False,
                is_public=False,
            ),
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, slug, style in [
                ("Puheohjelma: esitelmä / Presentation", "pres", "color1"),
                ("Puheohjelma: paneeli / Panel discussion", "panel", "color1"),
                ("Puheohjelma: keskustelu / Discussion group", "disc", "color1"),
                ("Työpaja: käsityö / Workshop: crafts", "craft", "color2"),
                ("Työpaja: figut / Workshop: miniature figurines", "mini", "color2"),
                ("Työpaja: musiikki / Workshop: music", "music", "color2"),
                ("Työpaja: muu / Other workshop", "workshop", "color2"),
                ("Tanssiohjelma / Dance programme", "dance", "color2"),
                ("Pelitiski: Figupeli / Miniature wargame", "miniwar", "color3"),
                ("Pelitiski: Korttipeli / Card game", "card", "color3"),
                ("Pelitiski: Lautapeli / Board game", "board", "color3"),
                ("Pelitiski: Muu / Other", "exp", "color3"),
                ("Roolipeli / Pen & Paper RPG", "rpg", "color4"),
                ("LARP", "larp", "color5"),
                ("Muu ohjelma / None of the above", "other", "color6"),
                ("Sisäinen ohjelma", "internal", "sisainen"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    slug=slug,
                    defaults=dict(
                        title=title,
                        style=style,
                        public=style != "sisainen",
                    ),
                )

        TimeBlock.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
            defaults=dict(
                end_time=self.event.end_time,
            ),
        )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

        have_views = View.objects.filter(event=self.event).exists()
        if not have_views:
            for view_name, room_names in [
                (
                    "Pääohjelmatilat",
                    [
                        "Halli 3 Ohjelmalava",
                        "Halli 3 Korttipelialue",
                        "Halli 3 Figupelialue",
                    ],
                ),
            ]:
                view, created = View.objects.get_or_create(event=self.event, name=view_name)

                if created:
                    rooms = [Room.objects.get(name__iexact=room_name, event=self.event) for room_name in room_names]

                    view.rooms = rooms
                    view.save()

        role = Role.objects.get(personnel_class__event=self.event, title="Roolipelinjohtaja")
        alternative_form, unused = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="roolipeli",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä / Call for GMs (tabletop role-playing games)",
                description=resource_string(__name__, "texts/roolipelit.html").decode("UTF-8"),
                programme_form_code="events.ropecon2020.forms:RpgForm",
                num_extra_invites=0,
                order=20,
                role=role,
            ),
        )

        # v90
        if alternative_form.role is None:
            alternative_form.role = role
            alternative_form.save()

        role = Role.objects.get(personnel_class__event=self.event, title="Larp-pelinjohtaja")
        alternative_form, unused = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="larp",
            defaults=dict(
                title="Tarjoa larppia / Call for Larps 2020",
                description=resource_string(__name__, "texts/larpit.html").decode("UTF-8"),
                programme_form_code="events.ropecon2020.forms:LarpForm",
                num_extra_invites=0,
                order=30,
                role=role,
            ),
        )

        # v90
        if alternative_form.role is None:
            alternative_form.role = role
            alternative_form.save()

        role = Role.objects.get(personnel_class__event=self.event, title="Peliohjelmanjärjestäjä")
        alternative_form, unused = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="pelitiski",
            defaults=dict(
                title="Tarjoa peliohjelmaa / Call for Game Programme 2020",
                short_description="Figupelit, korttipelit, lautapelit, Kokemuspiste ym. / Miniature wargames, card games, board games, Experience Point etc.",
                description=resource_string(__name__, "texts/pelitiski.html").decode("UTF-8"),
                programme_form_code="events.ropecon2020.forms:GamingDeskForm",
                num_extra_invites=0,
                order=60,
            ),
        )

        # v90
        if alternative_form.role is None:
            alternative_form.role = role
            alternative_form.save()

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelmanjärjestäjä")
        alternative_form, unused = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa muuta ohjelmaa / Offer any other program",
                short_description="Puheohjelmat, työpajat, esitykset ym. / Lecture program, workshops, show program etc.",
                description=resource_string(__name__, "texts/muuohjelma.html").decode("UTF-8"),
                programme_form_code="events.ropecon2020.forms:ProgrammeForm",
                num_extra_invites=0,
                order=300,
                role=role,
            ),
        )

        # v90
        if alternative_form.role is None:
            alternative_form.role = role
            alternative_form.save()

        for time_slot_name in [
            "Perjantaina iltapäivällä / Friday afternoon",
            "Perjantaina illalla / Friday evening",
            "Perjantain ja lauantain välisenä yönä / Friday night",
            "Lauantaina aamupäivällä / Saturday morning",
            "Lauantaina päivällä / Saturday noon",
            "Lauantaina iltapäivällä / Saturday afternoon",
            "Lauantaina illalla / Saturday evening",
            "Lauantain ja sunnuntain välisenä yönä / Saturday night",
            "Sunnuntaina aamupäivällä / Sunday morning",
            "Sunnuntaina päivällä / Sunday noon",
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

        for tag_title in [
            "Aloittelijaystävällinen",
            "Demo",
            "Ei sovellu lapsille",
            "Figupelaaminen",
            "In English",
            "Korttipelaaminen",
            "Kunniavieras",
            "Kutsuvieras",
            "Sopii lapsille",
            "Larppaaminen",
            "Lautapelaaminen",
            "Perheohjelma",
            "Pöytäroolipelaaminen",
            "Vain täysi-ikäisille",
            "Kovaääninen",
            "Teema",
            "Kilpailu/Turnaus",
        ]:
            Tag.objects.get_or_create(event=self.event, title=tag_title)

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            reference_number_template="2020{:06d}",
            contact_email="Ropecon 2020 -lipunmyynti <lipunmyynti@ropecon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Ropecon 2020 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
            "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
            "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
            "lipunvaihtopisteessä.\n\n"
            "Tervetuloa Ropeconiin!",
            front_page_text="<h2>Tervetuloa Ropeconin lippukauppaan!</h2>"
            "<p>Liput maksetaan tilauksen yhteydessä käyttämällä suomalaia verkkopankkipalveluja.</p>"
            "<p>Maksetut liput toimitetaan e-lippuina sähköpostitse asiakkaan antamaan osoitteeseen. E-liput vaihdetaan rannekkeiksi tapahtumaan saavuttaessa.</p>"
            "<p>Lisätietoja lipuista saat tapahtuman verkkosivuilta. <a href='https://2020.ropecon.fi/liput/'>Siirry takaisin tapahtuman verkkosivuille</a>.</p>"
            "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
            "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>lipunmyynti@ropecon.fi</em>",
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
                name="Ropecon 2020 Christmas Dragon -viikonloppulippu",
                description='Sisältää pääsyn Ropecon 2020 -tapahtumaan koko viikonlopun ajan. Jos haluat antaa lipun lahjaksi, voit ladata <a href="https://2020.ropecon.fi/wp-content/uploads/2019/11/joulukortti.pdf" target="_blank" rel="noopener nofollow">tästä</a> taitettavan kortin annettavaksi lipun kanssa.',
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=4000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2020 Lasten Christmas Dragon -viikonloppulippu",
                description='Sisältää pääsyn lapselle (7–12 v) Ropecon 2020 -tapahtumaan koko viikonlopun ajan. Jos haluat antaa lipun lahjaksi, voit ladata <a href="https://2020.ropecon.fi/wp-content/uploads/2019/11/joulukortti.pdf" target="_blank" rel="noopener nofollow">tästä</a> taitettavan kortin annettavaksi lipun kanssa.',
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2020 Perhelippu",
                description="Sisältää pääsyn Ropecon 2020 -tapahtumaan 2 aikuiselle ja 1–3 lapselle (7–12 v) koko viikonlopun ajan.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=9900,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2020 Early Dragon -viikonloppulippu",
                description="Sisältää pääsyn Ropecon 2020 -tapahtumaan koko viikonlopun ajan.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=4000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2020 Lasten Early Dragon -viikonloppulippu",
                description="Sisältää pääsyn lapselle (7–12 v) Ropecon 2020 -tapahtumaan koko viikonlopun ajan.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            # dict(
            #     name='Ropecon 2020 Sponsoriviikonloppulippu',
            #     description='Sisältää pääsyn Ropecon 2020 -tapahtumaan koko viikonlopun ajan.',
            #     limit_groups=[
            #         limit_group('Pääsyliput', 9999),
            #     ],
            #     price_cents=10000,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Ropecon 2020 Akateeminen seminaari + perjantaipäivälippu',
            #     description='Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2020 -tapahtumaan perjantaina. Muista myös <a href="https://goo.gl/forms/J9X1401lERxaX3M52">rekisteröityä</a>!',
            #     limit_groups=[
            #         limit_group('Pääsyliput', 9999),
            #     ],
            #     price_cents=5500,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
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
            ),
        )

    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta, Team

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
            ("tuottajat", "Tuottajat"),
            ("infra", "Infra"),
            ("palvelut", "Palvelut"),
            ("ohjelma", "Ohjelma"),
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


class Command(BaseCommand):
    args = ""
    help = "Setup ropecon2020 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
