from datetime import datetime, timedelta

import yaml
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils.timezone import now
from pkg_resources import resource_stream


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
        self.setup_programme()
        self.setup_program_v2()
        self.setup_intra()
        self.setup_access()
        self.setup_directory()
        # self.setup_kaatoilmo()
        self.setup_forms()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.organization, unused = Organization.objects.get_or_create(
            slug="tracon-ry",
            defaults=dict(
                name="Tracon ry",
                homepage_url="https://ry.tracon.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
        self.event, unused = Event.objects.get_or_create(
            slug="tracon2024",
            defaults=dict(
                name="Tracon (2024)",
                name_genitive="Traconin",
                name_illative="Traconiin",
                name_inessive="Traconissa",
                homepage_url="http://2024.tracon.fi",
                organization=self.organization,
                start_time=datetime(2024, 9, 6, 16, 0, tzinfo=self.tz),
                end_time=datetime(2024, 9, 8, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Event, Person
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
            Survey,
        )

        from ...models import Night, SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
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

        for pc_name, pc_slug, pc_app_label, pc_afterparty in [
            ("Coniitti", "coniitti", "labour", True),
            ("Duniitti", "duniitti", "labour", True),
            ("Vuorovastaava", "vuorovastaava", "labour", True),
            ("Työvoima", "tyovoima", "labour", True),
            ("Ohjelma", "ohjelma", "programme", True),
            ("Ohjelma 2. luokka", "ohjelma-2lk", "programme", False),
            ("Ohjelma 3. luokka", "ohjelma-3lk", "programme", False),
            (
                "Guest of Honour",
                "goh",
                "programme",
                False,
            ),  # tervetullut muttei kutsuta automaattiviestillä
            ("Media", "media", "badges", False),
            ("Myyjä", "myyja", "badges", False),
            ("Vieras", "vieras", "badges", False),
            ("Vapaalippu, viikonloppu", "vapaalippu-vkl", "tickets", False),
            ("Vapaalippu, lauantai", "vapaalippu-la", "tickets", False),
            ("Vapaalippu, sunnuntai", "vapaalippu-su", "tickets", False),
            ("Cosplaykisaaja", "cosplay", "tickets", False),
            ("AMV-kisaaja", "amv", "tickets", False),
            ("Taidekuja", "taidekuja", "tickets", False),
            ("Yhdistyspöydät", "yhdistyspoydat", "tickets", False),
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        coniitti = PersonnelClass.objects.get(event=self.event, slug="coniitti")

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
                signup_form_class_path="events.tracon2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.tracon2024.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for url, link_title, link_group in [
            (
                "https://wiki.tracon.fi/collection/tracon-2024-SWoEDT7utU",
                "Coniteawiki",
                "conitea",
            ),
            (
                "https://wiki.tracon.fi/collection/traconin-tyovoimawiki-Oinc2anefS",
                "Työvoimawiki",
                "accepted",
            ),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=url,
                    group=labour_event_meta.get_group(link_group),
                ),
            )

        assert self.event.start_time

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
                form_class_path="events.tracon2024.forms:ShiftWishesSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=60),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="swag",
            defaults=dict(
                title="Swag",
                description=(
                    "Tarjoamme työvoimatuotteeksi joko juomapullon tai paidan. Valitse tässä kumpi, "
                    "sekä paidan tapauksessa paitakokosi."
                ),
                form_class_path="events.tracon2024.forms:SwagSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=90),
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            due_days=14,
            reference_number_template="2024{:06d}",
            contact_email="Traconin lipunmyynti <liput@tracon.fi>",
            ticket_free_text=(
                "Tämä on sähköinen lippusi vuoden 2024 Traconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Traconiin!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Traconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2024.tracon.fi'>Traconin kotisivuilta</a>.</p>"
            ),
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
            #     name="Viikonloppulippu",
            #     description="Voimassa koko tapahtuman ajan perjantaista sunnuntaihin. Toimitetaan sähköpostitse PDF-tiedostona.",
            #     limit_groups=[
            #         limit_group("Perjantain liput", 5200),
            #         limit_group("Lauantain liput", 5200),
            #         limit_group("Sunnuntain liput", 5200),
            #     ],
            #     price_cents=4500,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Perjantailippu",
            #     description="Voimassa perjantaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
            #     limit_groups=[
            #         limit_group("Perjantain liput", 5200),
            #     ],
            #     price_cents=2000,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Lauantailippu",
            #     description="Voimassa lauantaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
            #     limit_groups=[
            #         limit_group("Lauantain liput", 5200),
            #     ],
            #     price_cents=3500,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Sunnuntailippu",
            #     description="Voimassa sunnuntaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
            #     limit_groups=[
            #         limit_group("Sunnuntain liput", 5200),
            #     ],
            #     price_cents=3000,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="K18 Iltabilelippu",
            #     description="Voimassa Traconin iltabileiden ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
            #     limit_groups=[
            #         limit_group("Iltabileliput", 1300),
            #     ],
            #     price_cents=1500,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Lattiamajoitus 1 yö pe–la – Amurin koulutalo (ei sis. makuualustaa)",
            #     description="Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Amurin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja. Majoituksesta ei tule erillistä PDF-lippua vaan sisään pääsee ilmoittamalla nimensä saapuessaan.",
            #     limit_groups=[
            #         limit_group("Majoitus Amuri pe-la", 235),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name="Lattiamajoitus 1 yö la–su – Amurin koulutalo (ei sis. makuualustaa)",
            #     description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Amurin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja. Majoituksesta ei tule erillistä PDF-lippua vaan sisään pääsee ilmoittamalla nimensä saapuessaan.",
            #     limit_groups=[
            #         limit_group("Majoitus Amuri la-su", 235),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Conitealippu",
                description="Teatterilippu <strong>Traconin conitean, Hitpointin conitean tai yhdistyksen hallituksen jäsenelle itselleen</strong> alennettuun hintaan.",
                limit_groups=[
                    limit_group("TSH-coniteanäytäntö", 90),
                ],
                price_cents=35_00,
                requires_accommodation_information=False,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Avec-lippu",
                description="Teatterilippu seuralaiselle ilman Tracon ry:n subventiota.",
                limit_groups=[
                    limit_group("TSH-coniteanäytäntö", 90),
                ],
                price_cents=75_00,
                requires_accommodation_information=False,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
                product.save()

        if not meta.receipt_footer:
            meta.receipt_footer = "Tracon ry / Y-tunnus 2886274-5 / liput@tracon.fi"
            meta.save()

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            Tag,
            TimeBlock,
        )

        from ...models import AccessibilityWarning, TimeSlot

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Traconin ohjelmatiimi <ohjelma@tracon.fi>",
                schedule_layout="full_width",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
            ("ohjelma-2lk", "Ohjelmanjärjestäjä (2. luokka)", False),
            ("ohjelma-3lk", "Ohjelmanjärjestäjä (3. luokka)", False),
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
                ("Animeohjelma", "anime"),
                ("Cosplayohjelma", "cosplay"),
                ("Miitti", "miitti"),
                ("Muu ohjelma", "muu"),
                ("Roolipeliohjelma", "rope"),
                ("Peliohjelma", "color7"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

        assert self.event.start_time
        assert self.event.end_time

        saturday = self.event.start_time + timedelta(days=1)

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=16, minute=0, tzinfo=self.tz),
                self.event.start_time.replace(hour=21, minute=0, tzinfo=self.tz),
            ),
            (
                saturday.replace(hour=9, minute=0, tzinfo=self.tz),
                self.event.end_time.replace(hour=1, minute=0, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=9, minute=0, tzinfo=self.tz),
                self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
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

        for time_slot_name in [
            "Perjantaina illalla",
            "Lauantaina päivällä",
            "Lauantaina iltapäivällä",
            "Lauantaina illalla",
            "Lauantain ja sunnuntain välisenä yönä",
            "Sunnuntaina aamupäivällä",
            "Sunnuntaina päivällä",
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

        for accessibility_warning in [
            "Välkkyviä valoja",
            "Kovia ääniä",
            "Savuefektejä",
        ]:
            AccessibilityWarning.objects.get_or_create(name=accessibility_warning)

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                programme_form_code="events.tracon2024.forms:RpgForm",
                num_extra_invites=0,
                order=10,
            ),
        )

        default_form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa puhe- tai muuta ohjelmaa",
                short_description="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole pöytäroolipeli.",
                programme_form_code="events.tracon2024.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.tracon2024.forms:ProgrammeForm"
            default_form.save()

        self.event.programme_event_meta.create_groups()

    def setup_program_v2(self):
        """
        This is for development purposes only. Once program v2 is up and running, there will be some
        default form that will be used to initialize the event, and a feature will be provided to copy
        forms from another event.
        """
        from forms.models import Form
        from program_v2.models import Dimension, OfferForm, ProgramV2EventMeta
        from programme.models import ProgrammeEventMeta

        category_dimension, _ = Dimension.objects.get_or_create(
            event=self.event,
            slug="category",
            defaults=dict(
                title=dict(
                    fi="Ohjelmatyyppi",
                    en="Category",
                ),
            ),
        )

        (programme_admin_group,) = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins"])
        ProgramV2EventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=programme_admin_group,
                primary_dimension=category_dimension,
            ),
        )

        with resource_stream("program_v2.models", "default_forms/fi.yml") as f:
            default_form_fi_fields = yaml.safe_load(f)["fields"]

        default_form_fi, _ = Form.objects.get_or_create(
            event=self.event,
            slug="program-default-fi",
            language="fi",
            defaults=dict(
                title="Tarjoa puhe- tai muuta ohjelmaa",
                fields=default_form_fi_fields,
            ),
        )

        with resource_stream("program_v2.models", "default_forms/en.yml") as f:
            default_form_en_fields = yaml.safe_load(f)["fields"]

        default_form_en, _ = Form.objects.get_or_create(
            event=self.event,
            slug="program-default-en",
            language="en",
            defaults=dict(
                title="Offer a talk or other programme item",
                fields=default_form_en_fields,
            ),
        )

        default_form, _ = OfferForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                short_description=dict(
                    fi="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole pöytäroolipeli.",
                    en="Select this option if your programme item is not a tabletop role-playing game.",
                ),
                active_from=now(),
            ),
        )

        if not default_form.languages.exists():
            default_form.languages.set([default_form_fi, default_form_en])

        rpg_form_fi, _ = Form.objects.get_or_create(
            event=self.event,
            slug="program-rpg-fi",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                language="fi",
                fields=[],
            ),
        )

        rpg_form_en, _ = Form.objects.get_or_create(
            event=self.event,
            slug="program-rpg-en",
            defaults=dict(
                title="Offer a tabletop role-playing game",
                language="en",
                fields=[],
            ),
        )

        rpg_form, _ = OfferForm.objects.get_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                short_description=dict(
                    fi="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi on pöytäroolipeli.",
                    en="Select this option if your programme item is a tabletop role-playing game.",
                ),
                active_from=now(),
            ),
        )

        if not rpg_form.languages.exists():
            rpg_form.languages.set([rpg_form_fi, rpg_form_en])

        Dimension.ensure_v1_default_dimensions(
            self.event,
            clear=False,
        )

        # leftover unattached forms that will come to haunt us at refresh_forms
        Form.objects.filter(event=self.event, slug__startswith="programme-").delete()

    def setup_access(self):
        from access.models import EmailAliasType, GroupEmailAliasGrant, GroupPrivilege, Privilege

        # Grant accepted workers access to Tracon Slack
        privilege = Privilege.objects.get(slug="tracon-slack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            self.event.programme_event_meta.get_group("hosts"),
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
            ("tracoff", "TracOff"),
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

            team, created = Team.objects.get_or_create(
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

    def setup_directory(self):
        from directory.models import DirectoryAccessGroup

        labour_admin_group = self.event.labour_event_meta.get_group("admins")

        assert self.event.end_time
        DirectoryAccessGroup.objects.get_or_create(
            organization=self.event.organization,
            group=labour_admin_group,
            active_from=now(),
            active_until=self.event.end_time + timedelta(days=30),
        )

    def setup_kaatoilmo(self):
        from labour.models import Survey
        from programme.models import Category, Programme, Room

        from ...models import Poison

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
                    "osallistua kaatajaisiin lauantaina 23. syyskuuta 2024 Tampereella. Kaatajaisiin osallistuminen edellyttää ilmoittautumista ja 18 vuoden ikää. "
                    "</p><p>"
                    "<strong>HUOM!</strong> Paikat kaatobusseihin varataan erikseen. Varaa paikkasi "
                    f'<a href="{outward_coach_url}" target="_blank" rel="noopener noreferrer">menobussiin täältä</a> ja '
                    f'<a href="{return_coach_url}" target="_blank" rel="noopener noreferrer">paluubussiin täältä</a>. '
                    f'Näet bussivarauksesi <a href="{reverse("programme:profile_reservations_view")}" target="_blank" rel="noopener noreferrer">paikkalippusivulta</a>.'
                ),
                override_does_not_apply_message=kaatoilmo_override_does_not_apply_message,
                form_class_path="events.tracon2024.forms:AfterpartyParticipationSurvey",
                active_from=self.event.end_time,
                active_until=datetime(2024, 9, 17, 23, 59, 59, tzinfo=self.tz),
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
        from forms.models.dimension import DimensionDTO
        from forms.models.form import Form
        from forms.models.survey import Survey

        # Hackathon feedback survey

        with resource_stream("events.tracon2024", "forms/hackathon-feedback.yml") as f:
            data = yaml.safe_load(f)

        hackathon_feedback_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="hackathon-feedback",
            language="fi",
            defaults=data,
        )

        # TODO(#386) remove when there is a form editor
        if not created:
            for key, value in data.items():
                setattr(hackathon_feedback_fi, key, value)
            hackathon_feedback_fi.save()

        hackathon_feedback_survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="hackathon-feedback",
            defaults=dict(
                active_from=now(),
            ),
        )

        hackathon_feedback_survey.languages.set([hackathon_feedback_fi])

        # Vendor signup form

        with resource_stream("events.tracon2024", "forms/vendor-signup-en.yml") as f:
            data = yaml.safe_load(f)

        vendor_signup_en, created = Form.objects.get_or_create(
            event=self.event,
            slug="vendor-signup-en",
            language="en",
            defaults=data,
        )

        # TODO(#386) remove when there is a form editor
        if not created:
            for key, value in data.items():
                setattr(vendor_signup_en, key, value)
            vendor_signup_en.save()

        with resource_stream("events.tracon2024", "forms/vendor-signup-fi.yml") as f:
            data = yaml.safe_load(f)

        vendor_signup_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="vendor-signup-fi",
            language="fi",
            defaults=data,
        )

        # TODO(#386) remove when there is a form editor
        if not created:
            for key, value in data.items():
                setattr(vendor_signup_fi, key, value)
            vendor_signup_fi.save()

        vendor_signup_survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="vendor-signup",
            defaults=dict(
                active_from=now(),
                key_fields=["name"],
            ),
        )

        vendor_signup_survey.languages.set([vendor_signup_fi, vendor_signup_en])

        with resource_stream("events.tracon2024", "forms/vendor-signup-dimensions.yml") as f:
            data = yaml.safe_load(f)

        for dimension in data:
            DimensionDTO.model_validate(dimension).save(vendor_signup_survey)

        # Expense claim form

        expense_claim_survey, _ = Survey.objects.update_or_create(
            event=self.event,
            slug="expense-claim",
            defaults=dict(
                active_from=now(),
                key_fields=["title"],
                login_required=True,
                anonymity="NAME_AND_EMAIL",
            ),
        )

        with resource_stream("events.tracon2024", "forms/expense-claim-dimensions.yml") as f:
            data = yaml.safe_load(f)

        dimensions = [DimensionDTO.model_validate(dimension) for dimension in data]
        DimensionDTO.save_many(expense_claim_survey, dimensions)

        with resource_stream("events.tracon2024", "forms/expense-claim-fi.yml") as f:
            data = yaml.safe_load(f)

        expense_claim_fi, created = Form.objects.update_or_create(
            event=self.event,
            slug="expense-claim-fi",
            language="fi",
            defaults=data,
        )

        # TODO(#386) remove when there is a form editor
        if not created:
            for key, value in data.items():
                setattr(expense_claim_fi, key, value)
            expense_claim_fi.save()

        expense_claim_survey.languages.set([expense_claim_fi])


class Command(BaseCommand):
    args = ""
    help = "Setup tracon2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
