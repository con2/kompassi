import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils import full_hours_between


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
        self.setup_badges()
        # self.setup_programme()
        self.setup_tickets()
        self.setup_intra()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Suvilahti (Helsinki)",
            defaults=dict(
                name_inessive="Suvilahdessa Helsingissä",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="finnish-fandom-conventions-ry",
            defaults=dict(
                name="Finnish Fandom Conventions ry",
                homepage_url="http://popcult.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="popcultday2024",
            defaults=dict(
                name="Popcult Day 2024",
                name_genitive="Popcult Day -tapahtuman",
                name_illative="Popcult Day -tapahtumaan",
                name_inessive="Popcult Day -tapahtumassa",
                homepage_url="https://popcult.fi/day-2024/",
                organization=self.organization,
                start_time=datetime(2024, 5, 18, 10, 0, tzinfo=self.tz),
                end_time=datetime(2024, 5, 18, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Event, Person
        from labour.models import AlternativeSignupForm, JobCategory, LabourEventMeta, PersonnelClass, Qualification

        from ...models import SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from core.models import Person

            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(hours=4),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email="Popcult Dayn työvoimavastaava <popcult@popcult.fi>",
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
            ("Vastaava", "vastaava", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Vieras", "vieras", "badges"),
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
                source_event=Event.objects.get(slug="popcult2019"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        JobCategory.objects.filter(event=self.event, slug="vastaava").update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications.set([qual])

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                title="Vastaavien ilmoittautumislomake",
                signup_form_class_path="events.popcultday2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.popcultday2024.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.start_time,
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

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2024{:06d}",
            contact_email="Popcult Day <liput@popcult.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Popcult Day 2024 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
            "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Popcult Day -tapahtumaan!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Popcult Day 2024 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='https://popcult.fi/day-2024/'>Popcult Day 2024 -tapahtuman kotisivuilta</a>.</p>",
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

        def ordering():
            ordering.counter += 10
            return ordering.counter

        ordering.counter = 0

        for product_info in [
            dict(
                name="Pääsylippu: Popcult Day 2024",
                description="Pääsylippu Popcult Day -tapahtumaan 18.5.2024 Helsingin Suvilahdessa. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Day", 600),
                ],
                price_cents=20_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Pääsylippu: Popcult Nights 2024",
                description="Pääsylippu Popcult Nights -iltatapahtumaan 18.5.2024 Helsingin Suvilahdessa. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Nights", 400),
                ],
                price_cents=15_00,
                electronic_ticket=True,
                available=False,
                ordering=ordering(),
            ),
            dict(
                name="Pääsylippu: Popcult Day + Nights 2024",
                description="Yhdistelmälippu Popcult Day & Nights -tapahtumiin 18.5.2024 Helsingin Suvilahdessa. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Day", 600),
                    limit_group("Nights", 400),
                ],
                price_cents=25_00,
                electronic_ticket=True,
                available=False,
                ordering=ordering(),
            ),
            dict(
                name="Pääsylippu: Popcult Nights 2024 (Day 2024 -lipun haltijalle)",
                description="HUOM! Voimassa vain yhdessä Popcult Day 2024 -lipun kanssa! Pääsylippu Popcult Nights -iltatapahtumaan 18.5.2024 Helsingin Suvilahdessa. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Nights", 400),
                ],
                price_cents=5_00,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
                code="nightsaddon-jhzdvxhd",  # will be changed in production
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import Category, ProgrammeEventMeta, Role, SpecialStartTime, Tag, TimeBlock

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Popcult Day -ohjelmatiimi <popcult@popcult.fi>",
                schedule_layout="reasonable",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        personnel_class = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

        role_priority = 0
        for role_title in [
            "Ohjelmanjärjestäjä",
            "Näkymätön ohjelmanjärjestäjä",
        ]:
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_title == "Ohjelmanjärjestäjä",
                    is_public=role_title != "Näkymätön ohjelmanjärjestäjä",
                    require_contact_info=True,
                    priority=role_priority,
                ),
            )
            role_priority += 10

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ("Puheohjelma", "color1"),
                ("Esitysohjelma", "color2"),
                ("Pajaohjelma", "color3"),
                ("Miitti", "color4"),
                ("Muu ohjelma", "color5"),
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
                self.event.start_time,
                self.event.start_time.replace(hour=21, minute=0, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=9, minute=0, tzinfo=self.tz),
                self.event.end_time,
            ),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

        for tag_title, tag_class in [
            ("In English", "label-success"),
            ("Ikärajasuositus K-15", "label-danger"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

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
            # ('vastaavat', 'Vastaavat'),
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


class Command(BaseCommand):
    args = ""
    help = "Setup popcultday2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
