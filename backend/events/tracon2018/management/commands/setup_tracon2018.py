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
        self.setup_tickets()
        self.setup_programme()
        self.setup_intra()
        self.setup_access()
        # self.setup_sms()

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
            slug="tracon2018",
            defaults=dict(
                name="Tracon (2018)",
                name_genitive="Traconin",
                name_illative="Traconiin",
                name_inessive="Traconissa",
                homepage_url="http://2018.tracon.fi",
                organization=self.organization,
                start_time=datetime(2018, 9, 8, 10, 0, tzinfo=self.tz),
                end_time=datetime(2018, 9, 9, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Person
        from core.utils import slugify
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
            Survey,
        )

        from ...models import Night, Poison, SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2018, 9, 7, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2018, 9, 9, 22, 0, tzinfo=self.tz),
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
            ("Guest of Honour", "goh", "programme", False),  # tervetullut muttei kutsuta automaattiviestillä
            ("Media", "media", "badges", False),
            ("Myyjä", "myyja", "badges", False),
            ("Vieras", "vieras", "badges", False),
            ("Vapaalippu, viikonloppu", "vapaalippu-vkl", "tickets", False),
            ("Vapaalippu, lauantai", "vapaalippu-la", "tickets", False),
            ("Vapaalippu, sunnuntai", "vapaalippu-su", "tickets", False),
            ("Cosplaykisaaja", "cosplay", "tickets", False),
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

        for name, description, pcs in [
            ("Conitea", "Tapahtuman järjestelytoimikunnan jäsen eli coniitti", [coniitti]),
            (
                "Järjestyksenvalvoja",
                "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa "
                "JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole "
                "täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
                [tyovoima],
            ),
            (
                "Info",
                "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman "
                "aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.",
                [tyovoima],
            ),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slugify(name),
                defaults=dict(
                    name=name,
                    description=description,
                ),
            )

            if created:
                job_category.personnel_classes.set(pcs)

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
                signup_form_class_path="events.tracon2018.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.tracon2018.forms:OrganizerSignupExtraForm",
                active_from=datetime(2017, 9, 16, 23, 8, 0, tzinfo=self.tz),
                active_until=datetime(2018, 9, 9, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            ("TERA", "Työvoimawiki", "accepted"),
            ("INFO", "Infowiki", "info"),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=f"https://atlasso.tracon.fi/crowd?next=https://confluence.tracon.fi/display/{wiki_space}",
                    group=labour_event_meta.get_group(link_group),
                ),
            )

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
                form_class_path="events.tracon2018.forms:ShiftWishesSurvey",
                active_from=datetime(2018, 7, 1, 16, 50, 0, tzinfo=self.tz),
                # active_until=datetime(2018, 8, 4, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        kaatoilmo_override_does_not_apply_message = (
            "Valitettavasti et pysty ilmoittautumaan kaatoon käyttäen tätä lomaketta. Tämä "
            "voi johtua siitä, että sinua ei ole kutsuttu kaatoon, tai teknisestä syystä. "
            "Kaatoon osallistumaan ovat oikeutettuja kaatopäivänä 18 vuotta täyttäneet "
            "coniitit, vuorovastaavat, vänkärit sekä badgelliset ohjelmanjärjestäjät. "
            "Mikäli saat tämän viestin siitä huolimatta, että olet mielestäsi oikeutettu "
            "osallistumaan kaatoon, ole hyvä ja ota sähköpostitse yhteyttä osoitteeseen "
            '<a href="mailto:kaatajaiset@tracon.fi">kaatajaiset@tracon.fi</a>.'
        )
        kaatoilmo, unused = Survey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen kaatajaisiin",
                description=(
                    "Kiitokseksi työpanoksestasi tapahtumassa Tracon tarjoaa sinulle mahdollisuuden "
                    "osallistua kaatajaisiin lauantaina 23. syyskuuta 2017 Hangaslahden saunalla "
                    "Tampereen lähistöllä. Kaatajaisiin osallistuminen edellyttää ilmoittautumista. "
                ),
                override_does_not_apply_message=kaatoilmo_override_does_not_apply_message,
                form_class_path="events.tracon2018.forms:AfterpartyParticipationSurvey",
                active_from=datetime(2018, 9, 13, 7, 57, 0, tzinfo=self.tz),
                active_until=datetime(2018, 9, 18, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for poison_name in [
            "Olut",
            "Siideri, kuiva",
            "Siideri, makea",
            "Lonkero",
            "Punaviini",
            "Valkoviini",
            "Cocktailit",
            "Alkoholittomat juomat",
        ]:
            Poison.objects.get_or_create(name=poison_name)

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
            reference_number_template="2018{:05d}",
            contact_email="Traconin lipunmyynti <liput@tracon.fi>",
            ticket_free_text=(
                "Tämä on sähköinen lippusi Traconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Traconiin!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Traconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2018.tracon.fi'>Traconin kotisivuilta</a>.</p>"
            ),
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2018, 7, 1, 18, 0, 0, tzinfo=self.tz),
            )
        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        # migration 0024_ticketseventmeta_pos_access_group
        if meta.pos_access_group is None:
            meta.pos_access_group = pos_access_group
            meta.save()

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
                description="Voimassa koko viikonlopun ajan la klo 10–02 ja su klo 07–18. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Lauantain liput", 4400),
                    limit_group("Sunnuntain liput", 4400),
                ],
                price_cents=2800,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lauantailippu",
                description="Voimassa koko lauantaipäivän ajan klo 10–02. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Lauantain liput", 4400),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Sunnuntailippu",
                description="Voimassa koko sunnuntaipäivän ajan klo 07–18. Toimitetaan sähköpostitse PDF-tiedostona.",
                limit_groups=[
                    limit_group("Sunnuntain liput", 4400),
                ],
                price_cents=1800,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Iltabilelippu",
                description="Pääsylippu maksullisiin K18-iltabileisiin Pakkahuoneella. Toimitetaan sähköpostitse PDF-tiedostona. Huomaathan, että tänä vuonna pääsy iltabileisiin edellyttää iltabilelipun lisäksi Traconin pääsylippua (lauantai-, sunnuntai- tai viikonloppulippu tai badge).",
                limit_groups=[
                    limit_group("Iltabileliput", 235),
                ],
                price_cents=500,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number() + 9000,  # XXX
            ),
            dict(
                name="Lattiamajoitus 1 yö pe-la - Aleksanterin koulu (sis. makuualusta)",
                description="Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.",
                limit_groups=[
                    limit_group("Majoitus Aleksanteri pe-la", 90),
                ],
                price_cents=1300,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoitus 1 yö la-su - Aleksanterin koulu (sis. makuualusta)",
                description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Aleksanterin koululta. Aleksanterin koulun majoituspaikat sisältävät makuualustan, joten sinun tarvitsee tuoda vain makuupussi.",
                limit_groups=[
                    limit_group("Majoitus Aleksanteri la-su", 90),
                ],
                price_cents=1300,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoitus 1 yö pe-la - Pyynikin koulu (ei sis. makuualustaa)",
                description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.",
                limit_groups=[
                    limit_group("Majoitus Pyynikki pe-la", 120),
                ],
                price_cents=1000,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoitus 1 yö la-su - Pyynikin koulu (ei sis. makuualustaa)",
                description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Pyynikin koululta. Pyynikin koulun majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.",
                limit_groups=[
                    limit_group("Majoitus Pyynikki la-su", 120),
                ],
                price_cents=1000,
                electronic_ticket=False,
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

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            Programme,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            Tag,
            TimeBlock,
            View,
        )

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Tracon -ohjelmatiimi <ohjelma@tracon.fi>",
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
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
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
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

        if self.test:
            # create some test programme
            Programme.objects.get_or_create(
                category=Category.objects.get(title="Animeohjelma", event=self.event),
                title="Yaoi-paneeli",
                defaults=dict(
                    description="Kika-kika tirsk",
                ),
            )

        for start_time, end_time in [
            (
                datetime(2018, 9, 7, 16, 0, tzinfo=self.tz),
                datetime(2018, 9, 7, 21, 0, tzinfo=self.tz),
            ),
            (
                datetime(2018, 9, 8, 9, 0, tzinfo=self.tz),
                datetime(2018, 9, 9, 1, 0, tzinfo=self.tz),
            ),
            (
                datetime(2018, 9, 9, 9, 0, tzinfo=self.tz),
                datetime(2018, 9, 9, 18, 0, tzinfo=self.tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

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
                        "Iso sali",
                        "Pieni sali",
                        "Sonaatti 1",
                        "Sonaatti 2",
                        "Duetto 2",
                        "Maestro",
                        "Puisto - Iso miittiteltta",
                        "Puisto - Pieni miittiteltta",
                    ],
                ),
            ]:
                for room_name in room_names:
                    Room.objects.get_or_create(event=self.event, name=room_name)

                rooms = [Room.objects.get(name__iexact=room_name, event=self.event) for room_name in room_names]

                view, created = View.objects.get_or_create(event=self.event, name=view_name)
                view.rooms = rooms
                view.save()

        for tag_title, tag_class in [
            ("Suositeltu", "hilight"),
            ("Musiikki", "label-info"),
            ("In English", "label-success"),
            ("K-18", "label-danger"),
            ("Paikkaliput", "label-warning"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                programme_form_code="events.tracon2018.forms:RpgForm",
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
                programme_form_code="events.tracon2018.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.tracon2018.forms:ProgrammeForm"
            default_form.save()

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

    # def setup_sms(self):
    #     from sms.models import SMSEventMeta

    #     sms_admin_group, = SMSEventMeta.get_or_create_groups(self.event, ['admins'])
    #     meta, unused = SMSEventMeta.objects.get_or_create(
    #         event=self.event,
    #         defaults=dict(
    #             admin_group=sms_admin_group,
    #             sms_enabled=True,
    #         )
    #     )

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
                defaults=dict(name=team_name, order=self.get_ordering_number(), group=team_group, email=email),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup tracon2018 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
