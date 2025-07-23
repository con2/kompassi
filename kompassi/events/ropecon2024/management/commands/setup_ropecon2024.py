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
            slug="ropecon2024",
            defaults=dict(
                name="Ropecon 2024",
                name_genitive="Ropecon 2024 -tapahtuman",
                name_illative="Ropecon 2024 -tapahtumaan",
                name_inessive="Ropecon 2024 -tapahtumassa",
                homepage_url="http://ropecon.fi",
                organization=self.organization,
                start_time=datetime(2024, 7, 19, 15, 0, tzinfo=self.tz),
                end_time=datetime(2024, 7, 21, 18, 0, tzinfo=self.tz),
                venue=self.venue,
                public=False,
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

        from ...models import Language, SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=23, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Ropecon 2024 -työvoimatiimi <tyovoima@ropecon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
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
                source_event=Event.objects.get(slug="ropecon2023"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            try:
                jc = JobCategory.objects.get(event=self.event, name=jc_name)
                qual = Qualification.objects.get(name=qualification_name)
            except JobCategory.DoesNotExist:
                pass

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
                signup_form_class_path="events.ropecon2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.ropecon2024.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="xxlomake",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.ropecon2024.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.ropecon2024.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Ropeconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella."
                ),
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
                contact_email="Ropecon 2024 -ohjelmatiimi <ohjelma@ropecon.fi>",
                schedule_layout="reasonable",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        if not Room.objects.filter(event=self.event).exists():
            for room_name in [
                "Pohjoinen aukio",
                "Pohjoisen sisäänkäynnin aula",
                "Ala-galleria",
                "Eteläisen sisäänkäynnin aula",
                "Messuaukio",
                "Lasigalleria",
                "Lastenhuone",
                "Säde",
                "Sali 102",
                "Sali 103",
                "Sali 104",
                "Sali 201",
                "Sali 203A",
                "Sali 203B",
                "Mesta",
                "Sali 204",
                "Sali 205",
                "Sali 206",
                "Sali 207",
                "Sali 208",
                "Sali 209",
                "Sali 210",
                "Sali 211",
                "Sali 212",
                "Sali 213",
                "Sali 214",
                "Sali 215",
                "Sali 216",
                "Sali 216A",
                "Sali 217",
                "Sali 218",
                "Sali 219",
                "Sali 301",
                "Sali 302",
                "Sali 303",
                "Sali 304",
                "Sali 305",
                "Sali 306",
                "Sali 307",
                "Halli 1 Spektaakkelisali",
                "Halli 1 Kahvila",
                "Halli 1B Työpajasali",
                "Halli 3 Kahvila",
                "Halli 3 Perhealue",
                "Halli 3 Boffaussali",
                "Halli 3 Tanssiharjoitussali",
                "Halli 3 Figualue",
                "Halli 3 Turnaussali",
                "Halli 3 Lautapelikirjaston pelialue",
                "Halli 3 Kokemuspiste",
                "Halli 3 Vapaa pelialue",
                "Halli 6B Myyntialue",
                "Halli 6B Näyttelyalue",
            ]:
                room, created = Room.objects.get_or_create(
                    event=self.event,
                    name=room_name,
                )

        # would normally be automatically created when meta.importer_name == "default"
        # but using custom importer opts out of it
        for room in Room.objects.filter(event=self.event):
            room.v2_dimensions = {"room": [room.slug]}
            room.save(update_fields=["v2_dimensions"])

        priority = 40
        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelma, päivä, ruoka", True),
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
            title="Ohjelma, päivä, ruoka, näkymätön",
            defaults=dict(
                override_public_title="Ohjelmanjärjestäjä",
                is_default=False,
                is_public=False,
                priority=50,
            ),
        )

        for input_data in [
            (
                "Puheohjelma: esitelmä / Presentation",
                "pres",
                "color1",
                {"type": ["talk", "presentation"]},
            ),
            (
                "Puheohjelma: paneeli / Panel discussion",
                "panel",
                "color1",
                {"type": ["talk", "panel"]},
            ),
            (
                "Puheohjelma: keskustelu / Discussion group",
                "disc",
                "color1",
                {"type": ["talk", "discussion"]},
            ),
            (
                "Työpaja: käsityö / Workshop: crafts",
                "workcraft",
                "color2",
                {
                    "type": ["workshop"],
                    "topic": ["crafts"],
                    "konsti": ["workshop"],
                },
            ),
            (
                "Työpaja: figut / Workshop: miniature figurines",
                "workmini",
                "color2",
                {
                    "type": ["workshop"],
                    "topic": ["miniatures"],
                    "konsti": ["workshop"],
                },
            ),
            (
                "Työpaja: musiikki / Workshop: music",
                "workmusic",
                "color2",
                {
                    "type": ["workshop"],
                    "topic": ["music"],
                    "konsti": ["workshop"],
                },
            ),
            (
                "Työpaja: muu / Workshop: other",
                "workother",
                "color2",
                {
                    "type": ["workshop"],
                    "konsti": ["workshop"],
                },
            ),
            (
                "Tanssiohjelma / Dance programme",
                "dance",
                "color2",
                {"type": ["activity"], "topic": ["dance"]},
            ),
            (
                "Esitysohjelma / Performance programme",
                "perforprog",
                "color2",
                {"type": ["performance"]},
            ),
            (
                "Miitti / Meetup",
                "meetup",
                "color2",
                {"type": ["meetup"]},
            ),
            (
                "Kokemuspiste: demotus / Experience Point: Demo game",
                "expdemo",
                "color3",
                {
                    "type": ["experience", "gaming", "demo"],
                    "konsti": ["experiencePoint"],
                },
            ),
            (
                "Kokemuspiste: avoin pelautus / Experience Point: Open game",
                "expopen",
                "color3",
                {
                    "type": ["experience", "gaming", "open-gaming"],
                    "konsti": ["experiencePoint"],
                },
            ),
            (
                "Kokemuspiste: muu / Experience Point: Other",
                "expother",
                "color3",
                {
                    "type": ["experience"],
                    "konsti": ["experiencePoint"],
                },
            ),
            (
                "Figupelit: demotus / Miniature wargames: Demo game",
                "minidemo",
                "color3",
                {
                    "type": ["gaming", "demo"],
                    "topic": ["miniatures"],
                    "konsti": ["other"],
                },
            ),
            (
                "Figupelit: avoin pelautus / Miniature wargames: Open game",
                "miniopen",
                "color3",
                {"type": ["gaming", "open-gaming"], "topic": ["miniatures"]},
            ),
            (
                "Turnaukset: figupelit / Tournament: Miniature wargames",
                "tourmini",
                "color3",
                {
                    "type": ["gaming", "tournament"],
                    "topic": ["miniatures"],
                    "konsti": ["tournament"],
                },
            ),
            (
                "Turnaukset: korttipelit / Tournament: Card games",
                "tourcard",
                "color3",
                {
                    "type": ["gaming", "tournament"],
                    "topic": ["cardgames"],
                    "konsti": ["tournament"],
                },
            ),
            (
                "Turnaukset: lautapelit / Tournament: Board games",
                "tourboard",
                "color3",
                {
                    "type": ["gaming", "tournament"],
                    "topic": ["boardgames"],
                    "konsti": ["tournament"],
                },
            ),
            (
                "Turnaukset: muu / Tournament: Other",
                "tourother",
                "color3",
                {
                    "type": ["gaming", "tournament"],
                    "konsti": ["tournament"],
                },
            ),
            (
                "Muu peliohjelma / Other game programme",
                "othergame",
                "color3",
                {"type": ["gaming"], "konsti": ["other"]},
            ),
            (
                "Roolipeli / Pen & Paper RPG",
                "rpg",
                "color4",
                {"type": ["gaming"], "topic": ["penandpaper"], "konsti": ["tabletopRPG"]},
            ),
            (
                "LARP",
                "larp",
                "color5",
                {"type": ["gaming"], "topic": ["larp"], "konsti": ["larp"]},
            ),
            (
                "Muu ohjelma / Other programme",
                "other",
                "color6",
                {"konsti": ["other"]},
            ),
            ("Sisäinen ohjelma", "internal", "sisainen"),
        ]:
            if len(input_data) == 3:
                title, slug, style = input_data
                v2_dimensions = {}
            elif len(input_data) == 4:
                title, slug, style, v2_dimensions = input_data
            else:
                raise ValueError(input_data)

            Category.objects.update_or_create(
                event=self.event,
                slug=slug,
                create_defaults=dict(
                    title=title,
                    style=style,
                    public=style != "sisainen",
                ),
                defaults=dict(
                    v2_dimensions=v2_dimensions,
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
                        "Halli 1 Spektaakkelisali",
                    ],
                ),
            ]:
                view, created = View.objects.get_or_create(event=self.event, name=view_name)

                if created:
                    rooms = [Room.objects.get(name__iexact=room_name, event=self.event) for room_name in room_names]

                    view.rooms = rooms
                    view.save()

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelma, päivä, ruoka")
        form, _ = AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="roolipeli",
            create_defaults=dict(
                title="Tarjoa pöytäroolipeliä / Call for GMs (tabletop role-playing games) 2024",
                description=resource_string(__name__, "texts/roolipelit.html").decode("UTF-8"),
                programme_form_code="events.ropecon2024.forms:RpgForm",
                num_extra_invites=2,
                order=20,
                role=role,
            ),
            defaults=dict(
                v2_dimensions={"topic": ["penandpaper"], "type": ["gaming"]},
            ),
        )

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelma, päivä, ruoka")
        form, _ = AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="larp",
            create_defaults=dict(
                title="Tarjoa larppia / Call for Larps 2024",
                description=resource_string(__name__, "texts/larpit.html").decode("UTF-8"),
                programme_form_code="events.ropecon2024.forms:LarpForm",
                num_extra_invites=2,
                order=30,
                role=role,
            ),
            defaults=dict(
                v2_dimensions={"topic": ["larp"], "type": ["gaming"]},
            ),
        )

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelma, päivä, ruoka")
        form, _ = AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="pelitiski",
            create_defaults=dict(
                title="Tarjoa peliohjelmaa / Call for Game Programme 2024",
                short_description="Figupelit, korttipelit, lautapelit, turnaukset, Kokemuspisteen pelit yms. / Miniature wargames, board games, card games, game tournaments, games at the Experience Point etc.",
                description=resource_string(__name__, "texts/pelitiski.html").decode("UTF-8"),
                programme_form_code="events.ropecon2024.forms:GamingDeskForm",
                num_extra_invites=3,
                order=60,
                role=role,
            ),
        )

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelma, päivä, ruoka")
        form, _ = AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="tyopaja",
            create_defaults=dict(
                title="Tarjoa työpajaohjelmaa / Call for Workshop Programme 2024",
                description=resource_string(__name__, "texts/tyopaja.html").decode("UTF-8"),
                programme_form_code="events.ropecon2024.forms:WorkshopForm",
                num_extra_invites=2,
                order=70,
                role=role,
            ),
            defaults=dict(
                v2_dimensions={"type": ["workshop"]},
            ),
        )

        role = Role.objects.get(personnel_class__event=self.event, title="Ohjelma, päivä, ruoka")
        form, _ = AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="default",
            create_defaults=dict(
                title="Tarjoa ohjelmaa Ropeconille / Call for Programme 2024",
                short_description="Puheohjelmat, esitykset ym. / Lecture program, show program etc.",
                description=resource_string(__name__, "texts/muuohjelma.html").decode("UTF-8"),
                programme_form_code="events.ropecon2024.forms:ProgrammeForm",
                num_extra_invites=2,
                order=300,
                role=role,
            ),
        )

        for time_slot_name in [
            "EI perjantaina iltapäivällä / NOT Friday afternoon",
            "EI perjantaina illalla / NOT Friday evening",
            "EI perjantain ja lauantain välisenä yönä / NOT Friday night",
            "EI lauantaina aamupäivällä / NOT Saturday morning",
            "EI lauantaina päivällä / NOT Saturday noon",
            "EI lauantaina iltapäivällä / NOT Saturday afternoon",
            "EI lauantaina illalla / NOT Saturday evening",
            "EI lauantain ja sunnuntain välisenä yönä / NOT Saturday night",
            "EI sunnuntaina aamupäivällä / NOT Sunday morning",
            "EI sunnuntaina päivällä / NOT Sunday noon",
            "EI sunnuntaina iltapäivällä / NOT Sunday afternoon",
            "Kaikki käy / Any time is fine",
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

        for tag_title, v2_dimensions in [
            ("Demo", {"type": ["demo"]}),
            ("Kilpailu/Turnaus", {"type": ["tournament"]}),
            ("Kunniavieras", {"topic": ["goh"]}),
            ("Aihe: Figupelit", {"topic": ["miniatures"]}),
            ("Aihe: Korttipelit", {"topic": ["cardgames"]}),
            ("Aihe: Larpit", {"topic": ["larp"]}),
            ("Aihe: Lautapelit", {"topic": ["boardgames"]}),
            ("Aihe: Pöytäroolipelit", {"topic": ["penandpaper"]}),
            ("Boffaus", {"topic": ["boffering"]}),
            ("Tanssiohjelma", {"topic": ["dance"]}),
            ("Liikunnallinen ohjelma", {"type": ["activity"]}),
        ]:
            Tag.objects.update_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    v2_dimensions=v2_dimensions,
                ),
            )

        self.event.programme_event_meta.create_groups()

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            reference_number_template="2024{:06d}",
            contact_email="Ropecon 2024 -lipunmyynti <lipunmyynti@ropecon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Ropecon 2024 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Ranneke tulee pitää ranteessa koko lipun\n"
            "voimassaoloajan. Voit tulostaa tämän lipun tai näyttää sen älypuhelimen tai tablettitietokoneen näytöltä.\n"
            "Mikäli kumpikaan näistä ei ole mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä\n"
            "sanasta koostuva Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Jos tapahtuma joudutaan perumaan, voit saada hyvityksen ottamalla yhteyttä: lipunmyynti@ropecon.fi. \n\n"
            "Tervetuloa Ropeconiin!\n\n"
            "---\n\n"
            "This is your electronic ticket to Ropecon 2024. The electronic ticket will be exchanged to a wrist band\n"
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
            dict(
                name="Ropecon 2024 Early Dragon viikonloppu / Weekend Ticket",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for the weekend.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=4000,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 lasten Early Dragon viikonloppu / Children's Weekend Ticket",
                description="Sisältää pääsyn lapselle (7-12v) Ropecon 2024 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for children (aged 7-12) for the weekend.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Early Dragon perhelippu (vkl) / Family Ticket (wknd)",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan 2 aikuiselle ja 1 - 3 lapselle (7-12 v) koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for two adults and 1-3 children (aged 7-12) for the weekend",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=9900,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 viikonloppu / Weekend Ticket",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for the weekend.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=4500,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 lasten viikonloppu / Children's Weekend Ticket",
                description="Sisältää pääsyn lapselle (7-12v) Ropecon 2024 -tapahtumaan koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for children (aged 7-12) for the weekend.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2500,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 perhelippu (vkl) / Family Ticket (wknd)",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan 2 aikuiselle ja 1 - 3 lapselle (7-12 v) koko viikonlopun ajan. / Includes the entrance to Ropecon 2024 for two adults and 1-3 children (aged 7-12) for the weekend",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=11000,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Academic Seminar and Friday Ticket",
                description="Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2024 -tapahtumaan perjantaina. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar and Ropecon 2024 on friday. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target='_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=5500,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Academic Seminar and Weekend Ticket",
                description="Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2024 -tapahtumaan koko viikonlopun ajan. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar and Ropecon 2024 for the weekend. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=6600,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Academic seminar",
                description="Sisältää pääsyn Akateemiseen seminaariin. Rekisteröitymislinkki: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a> / Includes the entrance to the Academic seminar. Please sign up to the event here: <a href='https://forms.gle/4KT3AHxKBBJWRTFa6' target=_blank'>https://forms.gle/4KT3AHxKBBJWRTFa6</a>",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2100,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Perjantai aikuinen / Friday Ticket ",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan perjantain ajan. / Includes the entrance to Ropecon 2024 for the Friday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=3400,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Lauantai aikuinen / Saturday Ticket",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan lauantain ajan. / Includes the entrance to Ropecon 2024 for the Saturday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=3400,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Sunnuntai aikuinen / Sunday Ticket",
                description="Sisältää pääsyn Ropecon 2024 -tapahtumaan sunnuntain ajan. / Includes the entrance to Ropecon 2024 for the Sunday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Perjantai lapsi / Children's Friday Ticket",
                description="Sisältää pääsyn lapselle (7-12v) Ropecon 2024 -tapahtumaan perjantain ajan. / Includes the entrance to Ropecon 2024 for children (aged 7-12) for the Friday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=1500,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Lauantai lapsi / Children's Saturday Ticket",
                description="Sisältää pääsyn lapselle (7-12v) Ropecon 2024 -tapahtumaan lauantain ajan. / Includes the entrance to Ropecon 2024 for children (aged 7-12) for the Saturday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=1500,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Sunnuntai lapsi / Children's Sunday Ticket",
                description="Sisältää pääsyn lapselle (7-12v) Ropecon 2024 -tapahtumaan sunnuntain ajan. / Includes the entrance to Ropecon 2024 for children (aged 7-12) for the Sunday.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Ropecon 2024 Haltiakummilippu / Fairy Godparent Ticket",
                description="Lahjoittaa viikonloppupääsyn Haltiakummilippua hakevalle Ropecon 2024 -tapahtumaan. HUOM: Tämä lahjoitustuote ei sisällä sisäänpääsyä itsellesi. / Buy this product to donate a ticket to someone who applies for a Godparent ticket. NOTE: This product does not include admission for yourself.",
                limit_groups=[
                    limit_group("Pääsyliput", 9999),
                ],
                price_cents=4000,
                electronic_ticket=False,
                available=False,
                ordering=self.get_ordering_number(),
                mail_description="\n".join(
                    line.strip()
                    for line in """
                        Kiitämme osallistumisestasi Haltiakummilippukeräykseen! <3
                        Haltiakummiliput jaetaan hakijoiden kesken heinäkuussa.

                        Thank you for participating in collection of Fairy Godparent tickets! <3
                        The tickets will be distributed among participants in July.
                    """.strip().splitlines()
                ),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
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
            ("talous", "Talous"),
            ("peliohjelma", "Peliohjelma"),
            ("ohjelma", "Ohjelma"),
            ("viestinta", "Viestintä"),
            ("tilatjatekniikka", "Tilat ja tekniikka"),
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


class Command(BaseCommand):
    args = ""
    help = "Setup ropecon2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
