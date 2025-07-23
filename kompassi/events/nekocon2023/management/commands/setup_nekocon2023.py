import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now


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
        # self.setup_tickets()
        # self.setup_programme()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Kuopion musiikkikeskus",
            defaults=dict(
                name_inessive="Kuopion musiikkikeskuksessa",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="nekocon-ry",
            defaults=dict(
                name="Nekocon ry",
                homepage_url="https://nekocon.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="nekocon2023",
            defaults=dict(
                name="Nekocon (2023)",
                name_genitive="Nekoconin",
                name_illative="Nekoconiin",
                name_inessive="Nekoconissa",
                homepage_url="https://nekocon.fi",
                organization=self.organization,
                start_time=datetime(2023, 7, 15, 10, 00, tzinfo=self.tz),
                end_time=datetime(2023, 7, 16, 17, 0, tzinfo=self.tz),
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
            WorkPeriod,
        )

        from ...models import Night, SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from kompassi.core.models import Person

            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=12, minute=0, tzinfo=self.tz) - timedelta(days=1),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Nekoconin työvoimatiimi <tyovoima@nekocon.fi>",
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
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Kunniavieras", "goh", "programme"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
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
        PersonnelClass.objects.get(event=self.event, slug="conitea")

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="nekocon2019"),
                target_event=self.event,
            )

            JobCategory.objects.filter(event=self.event, name="Conitea").update(public=False)

        labour_event_meta.create_groups()

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
            # (u'Green room', u'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            jc.required_qualifications.set([qual])

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Perjantain kasaus (pe klo 12–21)", None),
            ("Lauantain aamuvuoro (la klo 08–14)", None),
            ("Lauantain iltapäivävuoro (la klo 14–20)", None),
            ("Lauantain iltavuoro (la klo 20–02)", None),
            ("Lauantai–sunnuntai-yövuoro (su klo 02–08)", None),
            ("Sunnuntain aamuvuoro (su klo 08–14)", None),
            ("Sunnuntain iltapäivävuoro ja purku (su klo 14–20)", None),
        ]:
            WorkPeriod.objects.get_or_create(
                event=self.event,
                description=period_description,
                defaults=dict(
                    start_time=period_start,
                    end_time=(period_start + period_length) if period_start else None,
                ),
            )

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            "Perjantain ja lauantain välinen yö",
            "Lauantain ja sunnuntain välinen yö",
            # "Sunnuntain ja maanantain välinen yö",
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.nekocon2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.nekocon2023.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            ("NEKOCON2023", "Coniteawiki", "conitea"),
            # ('NEKOWORK', 'Työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=f"https://confluence.tracon.fi/display/{wiki_space}",
                    group=labour_event_meta.get_group(link_group),
                ),
            )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2023{:06}",
            contact_email="Nekocon (2023) <nekoconliput@gmail.com>",
            ticket_free_text="Tämä on sähköinen lippusi vuoden 2023 Nekoconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
            "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
            "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
            "lipunvaihtopisteessä.\n\n"
            "Tervetuloa Nekocon (2023) -tapahtumaan!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Nekoconiin!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://nekocon.fi'>Nekoconin kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
                max_count_per_product=5,
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        if meta.max_count_per_product == 99:
            meta.max_count_per_product = 5
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
                name="Nekocon (2023) -pääsylippu",
                description="Viikonloppuranneke Kuopiossa järjestettävään vuoden 2023 Nekoconiin. Huom. myynnissä vain viikonloppurannekkeita. E-lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Pääsyliput", 1800),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoituspaikka (koko vkl)",
                description="Lattiamajoituspaikka molemmiksi öiksi pe-la ja la-su. Majoitus aukeaa perjantaina 18:00 ja sulkeutuu sunnuntaina 12:00.",
                limit_groups=[
                    limit_group("Lattiamajoitus pe-la", 210),
                    limit_group("Lattiamajoitus la-su", 210),
                ],
                price_cents=1500,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoituspaikka (pe-la)",
                description="Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.nekocon.fi.",
                limit_groups=[
                    limit_group("Lattiamajoitus pe-la", 210),
                ],
                price_cents=1000,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name="Lattiamajoituspaikka (la-su)",
                description="Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.nekocon.fi.",
                limit_groups=[
                    limit_group("Lattiamajoitus la-su", 210),
                ],
                price_cents=1000,
                electronic_ticket=False,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            # dict(
            #     name='Nekocon (2023) -konserttilippu',
            #     description='Lippu Nekoconin konserttiin. Mikäli tarvitset pyörätuolipaikkaa, otathan ennen ostoa yhteyttä <em>liput@nekocon.fi</em>, jotta voimme varmistaa paikkatilanteen.',
            #     limit_groups=[
            #         limit_group('Konserttiliput', 820),
            #     ],
            #     price_cents=500,
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
            TimeBlock,
        )

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Nekoconin ohjelmatiimi <ohjelma@nekocon.fi>",
            ),
        )

        personnel_class = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

        role, unused = Role.objects.get_or_create(
            personnel_class=personnel_class,
            title="Ohjelmanjärjestäjä",
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            ),
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ("Anime ja manga", "anime"),
                ("Cosplay", "cosplay"),
                ("Paja", "miitti"),
                ("Muu ohjelma", "muu"),
                ("Kunniavieras", "rope"),
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
                self.event.start_time.replace(hour=10, minute=0),
                self.event.start_time.replace(hour=20, minute=0),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0),
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

        form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Ohjelmalomake",
                short_description="",
                programme_form_code="events.nekocon2023.forms:ProgrammeForm",
                num_extra_invites=0,
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


class Command(BaseCommand):
    args = ""
    help = "Setup nekocon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
