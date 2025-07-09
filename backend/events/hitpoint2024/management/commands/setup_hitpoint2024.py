from datetime import datetime, timedelta

import yaml
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils import full_hours_between
from core.utils.pkg_resources_compat import resource_stream


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
        self.setup_programme()
        self.setup_access()
        self.setup_badges()
        self.setup_forms()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Tredun Sammonkadun toimipiste",
            defaults=dict(
                name_inessive="Tredun Sammonkadun toimipisteessä",
            ),
        )
        self.organization = Organization.objects.get(slug="tracon-ry")
        self.event, unused = Event.objects.get_or_create(
            slug="hitpoint2024",
            defaults=dict(
                name="Tracon Hitpoint 2024",
                name_genitive="Tracon Hitpoint 2024 -tapahtuman",
                name_illative="Tracon Hitpoint 2024 -tapahtumaan",
                name_inessive="Tracon Hitpoint 2024 -tapahtumassa",
                homepage_url="http://2024.hitpoint.tracon.fi",
                organization=self.organization,
                start_time=datetime(2024, 11, 2, 10, 0, tzinfo=self.tz),
                end_time=datetime(2024, 11, 3, 18, 0, tzinfo=self.tz),
                venue=self.venue,
                public=True,
            ),
        )

        if self.event.start_time is None:
            self.event.start_time = datetime(2024, 11, 2, 10, 0, tzinfo=self.tz)
            self.event.end_time = datetime(2024, 11, 3, 18, 0, tzinfo=self.tz)
            self.event.public = True
            self.event.save()

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

        from ...models import SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, tzinfo=self.tz),  # type: ignore
            work_ends=self.event.end_time.replace(hour=23, minute=59, second=59, tzinfo=self.tz),  # type: ignore
            admin_group=labour_admin_group,
            contact_email="Tracon Hitpoint 2024 -työvoimatiimi <hitpoint@tracon.fi>",
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        conitea = PersonnelClass.objects.get(event=self.event, slug="conitea")
        ylivankari = PersonnelClass.objects.get(event=self.event, slug="ylivankari")
        ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="hitpoint2023"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
            ("Logistiikka", "Henkilöauton ajokortti (B)"),
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
                signup_form_class_path="events.hitpoint2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.hitpoint2024.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="swag",
            defaults=dict(
                title="Swag",
                description=("Syötä tässä paitakokosi, jos haluat työvoimapaidan."),
                form_class_path="events.hitpoint2024.forms:SwagSurvey",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for url, link_title, link_group in [
            (
                "https://wiki.tracon.fi/collection/hitpoint-2024-xSGNrS6PW9",
                "Coniteawiki",
                "conitea",
            ),
            (
                "https://wiki.tracon.fi/collection/hitpointin-tyovoimawiki-WjWtE61vAT",
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

        Survey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen kaatajaisiin",
                description=(
                    "Kiitokseksi työpanoksestasi tapahtumassa Tracon tarjoaa sinulle mahdollisuuden "
                    "osallistua kaatajaisiin lauantaina 20. tammikuuta 2024 Tampereella. Kaatajaisiin osallistuminen edellyttää ilmoittautumista ja 18 vuoden ikää. "
                ),
                form_class_path="events.hitpoint2024.forms:AfterpartyParticipationSurvey",
                active_from=self.event.end_time,
                active_until=datetime(2024, 1, 14, 23, 59, 59, tzinfo=self.tz),
            ),
        )

    def setup_programme(self):
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

        from ...models import TimeSlot

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Tracon Hitpoint -ohjelmatiimi <hitpoint.ohjelma@tracon.fi>",
                schedule_layout="reasonable",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
            # ('ohjelma-2lk', 'Ohjelmanjärjestäjä (2. luokka)', False),
            # ('ohjelma-3lk', 'Ohjelmanjärjestäjä (3. luokka)', False),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                ),
            )

        for title, slug, style, v2_dimensions in [
            ("Larppaaminen", "larp", "color1", {"topic": ["larp"]}),
            ("Lautapelit", "lautapelit", "color2", {"topic": ["boardgames"]}),
            ("Puheohjelma", "puheohjelma", "color3", {"type": ["talk"]}),
            ("Roolipeli", "roolipeli", "color4", {"topic": ["penandpaper"]}),
            ("Freeform", "freeform", "color1", {"topic": ["larp"]}),
            ("Korttipelit", "korttipelit", "color5", {"topic": ["cardgames"]}),
            ("Figupelit", "figupelit", "color6", {"topic": ["miniatures"]}),
            ("Muu ohjelma", "muu-ohjelma", "color7", {"topic": []}),  # nonfalsy to avoid default
            ("Sisäinen ohjelma", "sisainen-ohjelma", "sisainen", {"topic": []}),
        ]:
            Category.objects.update_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    title=title,
                    style=style,
                    public=style != "sisainen",
                    v2_dimensions=v2_dimensions,
                ),
            )

        for tag_slug, tag_title, v2_dimensions in [
            ("konsti-placeholder", "Konsti: Placeholder", {"konsti": []}),
            ("signup-rpg-desk", "Ilmoittautuminen roolipelitiskillä", {"signup": ["rpg-desk"]}),
        ]:
            Tag.objects.update_or_create(
                event=self.event,
                slug=tag_slug,
                defaults=dict(
                    title=tag_title,
                    style="label-default",
                    v2_dimensions=v2_dimensions,
                    public=False,
                ),
            )

        Tag.objects.filter(
            event=self.event,
            slug="sisainen-ohjelma",
        ).delete()

        for old_tag_slug, new_tag_slug in [
            ("figupelit", "miniatures"),
            ("korttipelit", "cardgames"),
            ("roolipeli", "penandpaper"),
            ("lautapelit", "boardgames"),
            ("puheohjelma", "talk"),
        ]:
            old_tag = Tag.objects.filter(event=self.event, slug=old_tag_slug).first()
            new_tag = Tag.objects.filter(event=self.event, slug=new_tag_slug).first()
            if old_tag and new_tag:
                for programme in old_tag.programme_set.all():
                    programme.tags.add(new_tag)
                old_tag.delete()

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),  # type: ignore
                self.event.end_time.replace(hour=1, minute=0, tzinfo=self.tz),  # type: ignore
            ),
            (
                self.event.end_time.replace(hour=9, minute=0, tzinfo=self.tz),  # type: ignore
                self.event.end_time.replace(hour=18, minute=0, tzinfo=self.tz),  # type: ignore
            ),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                description="",
                programme_form_code="events.hitpoint2024.forms:RpgForm",
                num_extra_invites=0,
                order=10,
                v2_dimensions={"type": ["gaming"], "topic": ["penandpaper"]},
            ),
        )

        AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="freeform",
            defaults=dict(
                title="Tarjoa larppia tai freeform-skenaariota",
                short_description="",
                programme_form_code="events.hitpoint2024.forms:FreeformForm",
                num_extra_invites=3,
                order=20,
                v2_dimensions={"type": ["gaming"], "topic": ["larp"]},
            ),
        )

        AlternativeProgrammeForm.objects.update_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa puhe- tai muuta ohjelmaa",
                short_description="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole roolipeli tai freeform-skenaario.",
                programme_form_code="events.hitpoint2024.forms:ProgrammeOfferForm",
                num_extra_invites=3,
                order=30,
            ),
        )

        for time_slot_name in [
            "Lauantaina päivällä",
            "Lauantaina illalla",
            "Sunnuntaina päivällä",
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

        TimeSlot.objects.filter(
            name__in=[
                "Lauantaina iltapäivällä",
                "Lauantain ja sunnuntain välisenä yönä",
                "Sunnuntaina aamupäivällä",
            ]
        ).delete()

        self.event.programme_event_meta.create_groups()

        for room in Room.objects.filter(event=self.event):
            room.v2_dimensions = {"room": [room.slug]}
            room.save(update_fields=["v2_dimensions"])

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2024{:06d}",
            contact_email="Tracon Hitpoint -lipunmyynti <hitpoint@tracon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Tracon Hitpoint -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
            "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
            "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
            "lipunvaihtopisteessä.\n\n"
            "Tervetuloa Tracon Hitpointiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Tracon Hitpoint -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla tai luottokortilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://2024.hitpoint.tracon.fi' target='_blank' rel='noreferrer noopener'>Tracon Hitpoint -tapahtuman kotisivuilta</a>.</p>"
            "<p><strong>Note</strong>: Purchasing Tracont Hitpoint tickets through this web shop requires a Finnish web bank service. "
            "If you do not have one, please contact us to purchase tickets: <em>hitpoint@tracon.fi</em>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),  # type: ignore
                ticket_sales_ends=t + timedelta(days=60),  # type: ignore
            )

        TicketsEventMeta.objects.update_or_create(
            event=self.event,
            create_defaults=defaults,
            defaults=dict(),
        )

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for product_info in [
            dict(
                name="Tracon Hitpoint -pääsylippu",
                description="Viikonloppulippu Tracon Hitpoint 2024 -tapahtumaan. Voimassa koko viikonlopun tapahtuman aukioloaikoina la klo 10–23:30 ja su klo 10–17. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia vastaan saat rannekkeen tapahtumaan saapuessasi.",
                limit_groups=[
                    limit_group("Pääsyliput", 500),
                ],
                price_cents=1200,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Tracon Hitpoint -kummilippu (Hope ry)",
                description="Kummilippu Tracon Hitpoint 2024 -tapahtumaan. Jokaista ostettua kummilippua kohti lahjoitamme koko viikonlopun lipun tapahtumaamme Hope ry:lle. Heidän kautttaan lahjaliput jaetaan vähävaraisille tai muista syistä lipun hankintaan tukea tarvitseville. HUOM! Tämä tuote ei sisällä sisäänpääsyä itsellesi Tracon Hitpointiin.",
                limit_groups=[
                    limit_group("Pääsyliput", 500),
                ],
                price_cents=1200,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)  # type: ignore
                product.save()

    def setup_access(self):
        from access.models import EmailAliasType, GroupEmailAliasGrant, GroupPrivilege, Privilege

        # Grant accepted workers access to Tracon Slack
        group = self.event.labour_event_meta.get_group("accepted")
        privilege = Privilege.objects.get(slug="tracon-slack")
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

    def setup_forms(self):
        from forms.models import Form, Survey
        from forms.models.meta import FormsEventMeta

        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])

        FormsEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="larp-survey",
            defaults=dict(
                active_from=now(),
            ),
        )

        with resource_stream("events.hitpoint2024", "forms/larp-survey-fi.yml") as f:
            data = yaml.safe_load(f)

        Form.objects.update_or_create(
            event=self.event,
            survey=survey,
            language="fi",
            defaults=data,
        )

        with resource_stream("events.hitpoint2024", "forms/larp-survey-en.yml") as f:
            data = yaml.safe_load(f)

        Form.objects.update_or_create(
            event=self.event,
            survey=survey,
            language="en",
            defaults=data,
        )

        if not survey.key_fields:
            survey.key_fields = ["participated_in_tracon_hitpoint"]
            survey.save()


class Command(BaseCommand):
    args = ""
    help = "Setup hitpoint2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
