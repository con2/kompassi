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
        # self.setup_payments()
        # self.setup_programme()
        self.setup_intra()
        # self.setup_access()
        # self.setup_kaatoilmo()
        # self.setup_sms()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.organization, unused = Organization.objects.get_or_create(
            slug="tracon-ry",
            defaults=dict(
                name="Tracon ry",
                homepage_url="https://ry.tracon.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
        self.event, unused = Event.objects.get_or_create(
            slug="tracon2021",
            defaults=dict(
                name="Tracon (2021)",
                name_genitive="Traconin",
                name_illative="Traconiin",
                name_inessive="Traconissa",
                homepage_url="http://2021.tracon.fi",
                organization=self.organization,
                start_time=datetime(2021, 9, 3, 16, 0, tzinfo=self.tz),
                end_time=datetime(2021, 9, 5, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Event, Person
        from kompassi.labour.models import (
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
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

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

        for pc_name, pc_slug, pc_app_label, _pc_afterparty in [
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

        PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        PersonnelClass.objects.get(event=self.event, slug="coniitti")

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
                signup_form_class_path="events.tracon2021.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.tracon2021.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            ("TRACON2021", "Coniteawiki", "conitea"),
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
                form_class_path="events.tracon2021.forms:ShiftWishesSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=60),
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

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ["admins", "pos"])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            reference_number_template="2021{:06d}",
            contact_email="Traconin lipunmyynti <liput@tracon.fi>",
            ticket_free_text=(
                "Tämä on sähköinen lippusi vuoden 2021 Traconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Traconiin!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Traconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2021.tracon.fi'>Traconin kotisivuilta</a>.</p>"
            ),
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
            # dict(
            #     name='Viikonloppulippu',
            #     description='Voimassa koko viikonlopun ajan la klo 09–00 ja su klo 09–18. Toimitetaan sähköpostitse PDF-tiedostona.',
            #     limit_groups=[
            #         limit_group('Lauantain liput', 4500),
            #         limit_group('Sunnuntain liput', 4500),
            #     ],
            #     price_cents=2800,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lauantailippu',
            #     description='Voimassa koko lauantaipäivän ajan klo 09–00. Toimitetaan sähköpostitse PDF-tiedostona.',
            #     limit_groups=[
            #         limit_group('Lauantain liput', 4500),
            #     ],
            #     price_cents=2000,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Sunnuntailippu',
            #     description='Voimassa koko sunnuntaipäivän ajan klo 09–18. Toimitetaan sähköpostitse PDF-tiedostona.',
            #     limit_groups=[
            #         limit_group('Sunnuntain liput', 4500),
            #     ],
            #     price_cents=1800,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Iltabilelippu',
            #     description='Pääsylippu maksullisiin K18-iltabileisiin Pakkahuoneella. Toimitetaan sähköpostitse PDF-tiedostona. Huomaathan, että tänä vuonna pääsy iltabileisiin edellyttää iltabilelipun lisäksi Traconin pääsylippua (lauantai-, sunnuntai- tai viikonloppulippu tai badge).',
            #     limit_groups=[
            #         limit_group('Iltabileliput', 235),
            #     ],
            #     price_cents=500,
            #     electronic_ticket=True,
            #     available=True,
            #     ordering=self.get_ordering_number() + 9000, # XXX
            # ),
            # dict(
            #     name='Lattiamajoitus 1 yö pe-la - Aleksanterin koulutalo (ei sis. makuualustaa)',
            #     description='Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Aleksanterin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
            #     limit_groups=[
            #         limit_group('Majoitus Aleksanteri pe-la', 100),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoitus 1 yö la-su - Aleksanterin koulutalo (ei sis. makuualustaa)',
            #     description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Aleksanterin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
            #     limit_groups=[
            #         limit_group('Majoitus Aleksanteri la-su', 100),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoitus 1 yö pe-la - Amurin koulutalo (ei sis. makuualustaa)',
            #     description='Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi Amurin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
            #     limit_groups=[
            #         limit_group('Majoitus Amuri pe-la', 195),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoitus 1 yö la-su - Amurin koulutalo (ei sis. makuualustaa)',
            #     description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi Amurin koulutalolta. Majoituspaikat eivät sisällä makuualustaa, joten sinun tarvitsee tuoda makuupussi ja makuualusta tai patja.',
            #     limit_groups=[
            #         limit_group('Majoitus Amuri la-su', 195),
            #     ],
            #     price_cents=1000,
            #     requires_accommodation_information=True,
            #     electronic_ticket=False,
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
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

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
                for minute in [15, 30, 45]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=minute),
                    )

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
                programme_form_code="events.tracon2021.forms:RpgForm",
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
                programme_form_code="events.tracon2021.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.tracon2021.forms:ProgrammeForm"
            default_form.save()

    def setup_access(self):
        from kompassi.access.models import (
            EmailAliasType,
            GroupEmailAliasGrant,
            GroupPrivilege,
            Privilege,
        )

        # Grant accepted workers access to Tracon Slack
        privilege = Privilege.objects.get(slug="tracon-slack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            # self.event.programme_event_meta.get_group("hosts"),
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
        from kompassi.labour.models import Survey
        from kompassi.zombies.programme.models import Category, Programme, Room

        from ...models import Poison

        saturday = self.event.start_time + timedelta(days=1)

        coaches = []
        for coach_title, room_title, hour in [
            # ('Kaatobussin paikkavaraus, menomatka', 'Kaatobussi meno', 15),
            # ('Kaatobussin paikkavaraus, paluumatka', 'Kaatobussi paluu', 23),
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

            # TODO remove for 2021
            if coach.is_paikkala_time_visible:
                coach.is_paikkala_time_visible = False
                coach.save()

            coach.paikkalize(
                max_tickets_per_user=1,
                max_tickets_per_batch=1,
                reservation_start=self.event.start_time,
                numbered_seats=False,
            )

            coaches.append(coach)

        # outward_coach, return_coach = coaches

        kaatoilmo_override_does_not_apply_message = (
            "Valitettavasti et pysty ilmoittautumaan kaatoon käyttäen tätä lomaketta. Tämä "
            "voi johtua siitä, että sinua ei ole kutsuttu kaatoon, tai teknisestä syystä. "
            "Kaatoon osallistumaan ovat oikeutettuja kaatopäivänä 18 vuotta täyttäneet "
            "coniitit, vuorovastaavat, vänkärit sekä badgelliset ohjelmanjärjestäjät. "
            "Mikäli saat tämän viestin siitä huolimatta, että olet mielestäsi oikeutettu "
            "osallistumaan kaatoon, ole hyvä ja ota sähköpostitse yhteyttä osoitteeseen "
            '<a href="mailto:kaatajaiset@tracon.fi">kaatajaiset@tracon.fi</a>.'
        )
        # outward_coach_url = reverse('programme:paikkala_reservation_view', args=(self.event.slug, outward_coach.id))
        # return_coach_url = reverse('programme:paikkala_reservation_view', args=(self.event.slug, return_coach.id))
        kaatoilmo, unused = Survey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen iltabileisiin",
                description=(
                    "Kiitokseksi työpanoksestasi tapahtumassa Tracon tarjoaa sinulle mahdollisuuden "
                    "osallistua iltabileisiin lauantaina 5. syyskuuta 2021 Tampereella. Iltabileisiin osallistuminen edellyttää ilmoittautumista. "
                    # '</p><p>'
                    # '<strong>HUOM!</strong> Paikat kaatobusseihin varataan erikseen. Varaa paikkasi '
                    # f'<a href="{outward_coach_url}" target="_blank">menobussiin täältä</a> ja '
                    # f'<a href="{return_coach_url}" target="_blank">paluubussiin täältä</a>. '
                    # f'Näet bussivarauksesi <a href="{reverse("profile_reservations_view")}" target="_blank">paikkalippusivulta</a>.'
                ),
                override_does_not_apply_message=kaatoilmo_override_does_not_apply_message,
                form_class_path="events.tracon2021.forms:AfterpartyParticipationSurvey",
                active_from=self.event.end_time,
                active_until=(self.event.end_time + timedelta(days=9)).replace(
                    hour=23, minute=59, second=59, tzinfo=self.tz
                ),
            ),
        )

        for poison_name in [
            # 'Olut',
            # 'Siideri, kuiva',
            # 'Siideri, makea',
            # 'Lonkero',
            # 'Panimosima',
            # 'Punaviini',
            # 'Valkoviini',
            # 'Cocktailit',
            # 'Alkoholittomat juomat',
        ]:
            Poison.objects.get_or_create(name=poison_name)


class Command(BaseCommand):
    args = ""
    help = "Setup tracon2021 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
