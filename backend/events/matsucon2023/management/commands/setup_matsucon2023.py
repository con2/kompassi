import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils import slugify


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
        self.setup_programme()
        self.setup_badges()
        self.setup_tickets()
        self.setup_intra()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Pohjankartanon koulu",
            defaults=dict(
                name_inessive="Pohjankartanon koululla",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="pohjoisten-conien-kyhaajat-ry",
            defaults=dict(
                name="Pohjoisten conien kyhääjät ry",
                homepage_url="http://matsucon.fi/pocky-ry/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="matsucon2023",
            defaults=dict(
                name="Matsucon 2023",
                name_genitive="Matsuconin",
                name_illative="Matsuconiin",
                name_inessive="Matsuconissa",
                homepage_url="http://matsucon.fi",
                organization=self.organization,
                start_time=datetime(2023, 10, 28, 10, 0, tzinfo=self.tz),
                end_time=datetime(2023, 10, 29, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Person
        from labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )

        from ...models import SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from core.models import Person

            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email="Matsuconin työvoimavastaava <matsuconfi@gmail.com>",
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
            ("Conitea", "coniitti", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Guest of Honour", "goh", "badges"),
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        coniitti = PersonnelClass.objects.get(event=self.event, slug="coniitti")

        for name, description, pcs in [
            (
                "Conitea",
                "Tapahtuman järjestelytoimikunnan jäsen eli coniitti",
                [coniitti],
            ),
            (
                "Järjestyksenvalvoja",
                "Järjestyksenvalvojan tehtäviin kuuluvat lippujen tarkistus, kulunvalvonta sekä ihmisten ohjaus. Tehtävään vaaditaan JV-kortti.",
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

        labour_event_meta.create_groups()

        JobCategory.objects.filter(event=self.event, slug="conitea").update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications.set([qual])

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.matsucon2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.matsucon2023.forms:OrganizerSignupExtraForm",
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

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            TimeBlock,
        )

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Matsuconin ohjelmavastaava <ohjelmavastaava@matsucon.fi>",
            ),
        )

        personnel_class = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

        role_priority = 0
        for role_title in [
            "Ohjelmanjärjestäjä",
            "Näkymätön ohjelmanjärjestäjä",
        ]:
            Role.objects.get_or_create(
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
                ("Anime ja manga", "color1"),
                ("Cosplay", "color2"),
                ("Pelit", "color3"),
                ("Japani", "color4"),
                ("Show", "color5"),
                ("Työpaja", "color6"),
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
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.end_time,
            ),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

        SpecialStartTime.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
        )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

    def setup_tickets(self):
        from tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2023{:06d}",
            contact_email="Matsucon <matsuconfi@gmail.com>",
            ticket_free_text="Tämä on sähköinen lippusi Matsucon 2023 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
            "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Matsuconhin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Matsucon 2023 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://matsucon.fi'>Matsucon 2023 -tapahtuman kotisivuilta</a>.</p>",
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
                name="Viikonloppulippu",
                description="Viikonloppulippu oikeuttaa sisäänpääsyn molempiin Matsuconin päiviin. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Viikonloppuliput", 550),
                ],
                price_cents=1800,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Lauantailippu",
                description="Lauantailippu oikeuttaa sisäänpääsyyn Matsuconin ensimmäiseen päivään. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Lauantailiput", 300),
                ],
                price_cents=1200,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Sunnuntailippu",
                description="Sunnuntailippu oikeuttaa sisäänpääsyyn Matsuconin toiseen päivään. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Sunnuntailiput", 150),
                ],
                price_cents=1200,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Iltabilelippu",
                description="Iltabilelippu oikeuttaa sisäänpääsyyn Matsuconin iltabileisiin tapahtuman lauantai-iltana.",
                limit_groups=[
                    limit_group("Iltabileliput", 120),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            # dict(
            #     name="Lattiamajoitus",
            #     description="Lattiamajoitus lauantain ja sunnuntain väliselle yölle tapahtumapaikalla.",
            #     limit_groups=[
            #         limit_group("Lattiamajoituspaikat", 35),
            #     ],
            #     price_cents=700,
            #     electronic_ticket=False,
            #     requires_accommodation_information=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
            # dict(
            #     name="Lattiamajoitus + aamiainen",
            #     description="Lattiamajoitus sekä aamiainen lauantain ja sunnuntain väliselle yölle tapahtumapaikalla.",
            #     limit_groups=[
            #         limit_group("Lattiamajoituspaikat", 35),
            #         limit_group("Aamiainen", 35),
            #     ],
            #     price_cents=1000,
            #     electronic_ticket=False,
            #     requires_accommodation_information=True,
            #     available=True,
            #     ordering=ordering(),
            # ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)

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
    help = "Setup matsucon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
