from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.utils import full_hours_between


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
        # self.setup_programme()
        # self.setup_tickets()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Espoon kulttuurikeskus",
            defaults=dict(
                name_inessive="Espoon kulttuurikeskuksessa",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="cosvision-ry",
            defaults=dict(
                name="Cosvision ry",
                homepage_url="https://www.cosvision.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="cosvision2023",
            defaults=dict(
                name="Cosvision (2023)",
                name_genitive="Cosvisionissa",
                name_illative="Cosvisioniin",
                name_inessive="Cosvisionissa",
                homepage_url="http://www.cosvision.fi",
                organization=self.organization,
                start_time=datetime(2023, 11, 25, 10, 0, tzinfo=self.tz),
                end_time=datetime(2023, 11, 25, 19, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
        from kompassi.labour.models import (
            AlternativeSignupForm,
            LabourEventMeta,
            PersonnelClass,
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
            work_ends=self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Cosvision <info@cosvision.fi>",
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

        for pc_name, pc_slug, pc_app_label in [
            ("Vastaavat", "vastaava", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Guest of Honour", "goh", "programme"),
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

        PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        PersonnelClass.objects.get(event=self.event, slug="vastaava")

        # if not JobCategory.objects.filter(event=self.event).exists():
        #     JobCategory.copy_from_event(
        #         source_event=Event.objects.get(slug="cosvision2022"),
        #         target_event=self.event,
        #     )

        # for name in ["Vastaava"]:
        #     JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        # for jc_name, qualification_name in [
        #     # ("Järjestyksenvalvoja", "JV-kortti"),
        # ]:
        #     jc = JobCategory.objects.get(event=self.event, name=jc_name)
        #     qual = Qualification.objects.get(name=qualification_name)

        #     jc.required_qualifications.set([qual])

        labour_event_meta.create_groups()

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
                signup_form_class_path="events.cosvision2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.cosvision2023.forms:OrganizerSignupExtraForm",
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
                contact_email="Cosvision <info@cosvision.fi>",
                schedule_layout="reasonable",
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
                ("Esitys", "color1"),
                ("Jatkuva ohjelma", "color2"),
                ("Osallistava ohjelma", "color3"),
                ("Työpaja", "color4"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

        saturday_start = (self.event.end_time - timedelta(days=1)).replace(hour=10, minute=0, tzinfo=self.tz)
        saturday_end = saturday_start.replace(hour=18, minute=0, tzinfo=self.tz)
        sunday_start = self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz)
        sunday_end = self.event.end_time.replace(hour=18, minute=0, tzinfo=self.tz)

        for start_time, end_time in [
            (saturday_start, saturday_end),
            (sunday_start, sunday_end),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30),  # look, no tz
                )

        for tag_title, tag_class in [
            ("Suositeltu", "hilight"),
            ("In English", "label-success"),
            ("Paikkaliput", "label-warning"),
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
                title="Tarjoa ohjelmaa",
                short_description="Tämän ohjetekstin ei pitäisi näkyä kenellekään.",
                programme_form_code="events.cosvision2023.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2023{:05d}",
            contact_email="Cosvision <info@cosvision.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Cosvision 2023 -tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Cosvisioniin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Cosvision 2023 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://popcult.fi/nights-2023'>Cosvision 2023 -tapahtuman kotisivuilta</a>.</p>",
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
                name="Päivälippu – Cosvision (2023)",
                description="Sisältää pääsylipun tapahtuma-alueelle ja oikeuden osallistua tapahtumassa järjestettävään ohjelmaan. Lippu toimitetaan pdf-tiedostona, joka vaihdetaan tapahtumassa rannekkeeseen.",
                limit_groups=[
                    limit_group("Pääsyliput", 700),
                ],
                price_cents=2150,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
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
            ),
        )

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
            ("vastaavat", "Vastaavat"),
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
    help = "Setup cosvision2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
