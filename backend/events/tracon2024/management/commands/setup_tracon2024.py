from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils.timezone import now

from core.utils import slugify


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
        self.setup_tickets()
        self.setup_programme()
        self.setup_program_v2()
        self.setup_intra()
        self.setup_access()
        self.setup_kaatoilmo()
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

        from badges.emperkelators.tracon2024 import TicketType, TraconEmperkelator
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
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
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
                "programme",
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
        meta, unused = BadgesEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
                emperkelator_name="tracon2024",
            ),
        )

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
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
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla, maksukortilla tai MobilePaylla heti tilauksen yhteydessä.</p>"
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
            dict(
                name="Viikonloppulippu",
                description="Voimassa koko tapahtuman ajan perjantaista sunnuntaihin. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Perjantain liput", 3860),
                    limit_group("Lauantain liput", 3860),
                    limit_group("Sunnuntain liput", 3860),
                ],
                price_cents=50_00,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Perjantailippu",
                description="Voimassa perjantaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Perjantain liput", 3860),
                ],
                price_cents=25_00,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lauantailippu",
                description="Voimassa lauantaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Lauantain liput", 3860),
                ],
                price_cents=40_00,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Sunnuntailippu",
                description="Voimassa sunnuntaina tapahtuman aukiolon ajan. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Sunnuntain liput", 3860),
                ],
                price_cents=35_00,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="K18 Iltabilelippu",
                description="Voimassa Traconin iltabileiden ajan. Huomioithan, että bileiden ikäraja on 18 vuotta. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Iltabileliput", 1200),
                ],
                price_cents=20_00,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoitus 1 yö pe–la – Fista, Tampereen kansainvälinen koulutalo",
                description="Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Fistan koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja. Majoituksesta ei tule erillistä PDF-lippua vaan sisään pääsee ilmoittamalla nimensä saapuessaan.",
                limit_groups=[
                    limit_group("Majoitus Fista pe-la", 220),
                ],
                price_cents=12_00,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoitus 1 yö la–su – Fista, Tampereen kansainvälinen koulutalo",
                description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Fistan koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja. Majoituksesta ei tule erillistä PDF-lippua vaan sisään pääsee ilmoittamalla nimensä saapuessaan.",
                limit_groups=[
                    limit_group("Majoitus Fista la-su", 220),
                ],
                price_cents=12_00,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Conitealippu",
                description="Teatterilippu <strong>Traconin conitean, Hitpointin conitean tai yhdistyksen hallituksen jäsenelle itselleen</strong> alennettuun hintaan.",
                limit_groups=[
                    limit_group("TSH-coniteanäytäntö", 90),
                ],
                price_cents=35_00,
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
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Väliaikatarjoilu: Katkarapuleipä",
                description="Laktoositon, saatavilla gluteeniton (ilmoita erikoisruokavaliosta Haiskulle/Dennulle)",
                limit_groups=[
                    limit_group("TSH-väliaikatarjoilut", 9999),
                ],
                price_cents=14_00,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Väliaikatarjoilu: Mordor-leivos",
                description="Laktoositon, gluteeniton",
                limit_groups=[
                    limit_group("TSH-väliaikatarjoilut", 9999),
                ],
                price_cents=9_00,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Väliaikatarjoilu: Kahvi",
                limit_groups=[
                    limit_group("TSH-väliaikatarjoilut", 9999),
                ],
                price_cents=4_50,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Väliaikatarjoilu: Tee",
                limit_groups=[
                    limit_group("TSH-väliaikatarjoilut", 9999),
                ],
                price_cents=4_50,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Taru sormusten herrasta 20.9.2024 – Väliaikatarjoilu: Kuohuviini",
                description="Piccolo (20 cl). Katetaan 1 lasin kanssa; pyydä tarvittaessa toinen lasi ravintolan henkilökunnalta.",
                limit_groups=[
                    limit_group("TSH-väliaikatarjoilut", 9999),
                ],
                price_cents=13_50,
                electronic_ticket=False,
                available=True,
                code="tsh-rcjxrpwl",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Conitean edustushupparin omavastuu",
                description="Käytä tätä tuotetta vain jos olet jo tilannut itsellesi hupparin aiemmin ohjeistetulla tavalla.",
                limit_groups=[
                    limit_group("Edustustuotteet", 9999),
                ],
                price_cents=19_00,
                electronic_ticket=False,
                available=True,
                code="hup-hvltvckn",  # will be changed in production
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
                product.save()

    def setup_programme(self):
        from badges.emperkelators.tracon2024 import TicketType, TraconEmperkelator
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
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

        for pc_slug, role_title, role_is_default, perks in [
            (
                "ohjelma",
                "Ohjelmanjärjestäjä",
                True,
                TraconEmperkelator(ticket_type=TicketType.INTERNAL_BADGE, meals=1, swag=True),
            ),
            (
                "ohjelma",
                "Esiintyjä",
                False,
                TraconEmperkelator(ticket_type=TicketType.INTERNAL_BADGE, meals=1, swag=True),
            ),
            (
                "ohjelma",
                "Keskustelunvetäjä",
                False,
                TraconEmperkelator(ticket_type=TicketType.INTERNAL_BADGE, meals=1, swag=False),
            ),
            (
                "ohjelma",
                "Työpajanvetäjä",
                False,
                TraconEmperkelator(ticket_type=TicketType.INTERNAL_BADGE, meals=1, swag=False),
            ),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            perks_dict = perks.model_dump()
            Role.objects.update_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                    perks=perks_dict,
                ),
            )

            Role.objects.update_or_create(
                personnel_class=personnel_class,
                title=f"Näkymätön {role_title.lower()}",
                defaults=dict(
                    override_public_title=role_title,
                    is_default=False,
                    is_public=False,
                    perks=perks_dict,
                ),
            )

        for title, style in [
            ("Animeohjelma", "anime"),
            ("Cosplayohjelma", "cosplay"),
            ("Miitti", "miitti"),
            ("Muu ohjelma", "muu"),
            ("Roolipeliohjelma", "rope"),
            ("Peliohjelma", "color7"),
        ]:
            Category.objects.update_or_create(
                event=self.event,
                style=style,
                defaults=dict(
                    title=title,
                    v2_dimensions={"category": [slugify(title)]},
                ),
            )

        assert self.event.start_time
        assert self.event.end_time

        saturday = self.event.start_time + timedelta(days=1)

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=15, minute=0, tzinfo=self.tz),
                saturday.replace(hour=0, minute=0, tzinfo=self.tz),
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

        # truthy "empty" value to opt out of automatic dimensions
        no_tags = {"accessibility": []}
        for tag_title, tag_class, v2_dimensions in [
            ("Suositeltu", "hilight", no_tags),
            ("Musiikki", "label-info", no_tags),
            ("In English", "label-success", {"language": ["en"]}),
            ("English OK", "label-success", {"language": ["fi", "en"]}),
            ("K-18", "label-danger", {"audience": ["r18"]}),
            ("Paikkaliput", "label-default", {"signup": ["paikkala"]}),
            ("Kirkkaita/välkkyviä valoja", "label-warning", {"accessibility": ["flashing-lights"]}),
            ("Kovia ääniä", "label-warning", {"accessibility": ["loud-noises"]}),
            ("Savutehosteita", "label-warning", {"accessibility": ["smoke-effects"]}),
            ("Konsti: Kirpputori", "label-default", {"konsti": ["fleamarket"]}),
            ("Konsti: Larppi", "label-default", {"konsti": ["larp"]}),
            ("Konsti: Placeholder", "label-default", {}),
        ]:
            Tag.objects.update_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                    v2_dimensions=v2_dimensions,
                    public=":" not in tag_title,
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

        AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                programme_form_code="events.tracon2024.forms:RpgForm",
                num_extra_invites=0,
                order=10,
                v2_dimensions={"konsti": ["tabletopRPG"]},
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

        for room in Room.objects.filter(event=self.event):
            room.v2_dimensions = {"room": [room.slug]}
            room.save(update_fields=["v2_dimensions"])

    def setup_program_v2(self):
        from program_v2.models.meta import ProgramV2EventMeta

        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=self.event.programme_event_meta.admin_group,
            ),
        )

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
        from forms.models.survey import SurveyDTO

        for survey in [
            SurveyDTO(
                slug="artisan-application",
                key_fields=["name", "email", "helper"],
            ),
            SurveyDTO(
                slug="artist-alley-application",
                key_fields=["name", "email", "artist_name1", "location", "reserve"],
            ),
            SurveyDTO(
                slug="expense-claim",
                key_fields=["title", "amount"],
                login_required=True,
                anonymity="NAME_AND_EMAIL",
            ),
            SurveyDTO(slug="hackathon-feedback"),
            SurveyDTO(slug="jv-kertauskurssi"),
            SurveyDTO(
                slug="opening-closing-performer-application",
                key_fields=["performer-name"],
            ),
            SurveyDTO(
                slug="vendor-application",
                key_fields=["name"],
            ),
            SurveyDTO(
                slug="cosplay-jury-application",
                key_fields=["performer_name"],
                login_required=True,
                anonymity="NAME_AND_EMAIL",
            ),
            SurveyDTO(
                slug="virkistyspaiva",
                login_required=True,
                anonymity="NAME_AND_EMAIL",
            ),
            SurveyDTO(
                slug="geekjam-signup",
                key_fields=["nick", "instruments"],
            ),
        ]:
            survey.save(self.event)


class Command(BaseCommand):
    args = ""
    help = "Setup tracon2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
