import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.utils import slugify


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
        # self.setup_tickets()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Pohjankartanon koulu",
            defaults=dict(
                name_inessive="Pohjankartanon koululla",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="pohjoisten-conien-kyhaajat-ry",
            defaults=dict(
                name="Pohjoisten conien kyhääjät r",
                homepage_url="http://matsucon.fi/pocky-ry/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="matsucon2018",
            defaults=dict(
                name="Matsucon 2018",
                name_genitive="Matsucon 2018 -tapahtuman",
                name_illative="Matsucon 2018 -tapahtumaan",
                name_inessive="Matsucon 2018 -tapahtumassa",
                homepage_url="http://matsucon.fi",
                organization=self.organization,
                start_time=datetime(2018, 5, 26, 10, 0, tzinfo=self.tz),
                end_time=datetime(2018, 5, 27, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
        from kompassi.labour.models import (
            AlternativeSignupForm,
            Job,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )

        from ...models import SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from kompassi.core.models import Person

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

        for jc_data in [
            ("Conitea", "Tapahtuman järjestelytoimikunnan jäsen eli coniitti", [coniitti]),
            (
                "Järjestyksenvalvoja",
                "Järjestyksenvalvojan tehtäviin kuuluvat lippujen tarkistus, kulunvalvonta sekä ihmisten ohjaus. Tehtävään vaaditaan JV-kortti.",
                [tyovoima],
            ),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                job_names = []
            elif len(jc_data) == 4:
                name, description, pcs, job_names = jc_data
            else:
                raise ValueError("Length of jc_data must be 3 or 4")

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

            for job_name in job_names:
                job, created = Job.objects.get_or_create(
                    job_category=job_category,
                    slug=slugify(job_name),
                    defaults=dict(
                        title=job_name,
                    ),
                )

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
                signup_form_class_path="events.matsucon2018.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.matsucon2018.forms:OrganizerSignupExtraForm",
                active_from=datetime(2018, 1, 21, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

    def setup_badges(self):
        from kompassi.badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
            ),
        )

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2018{:05d}",
            contact_email="Matsucon <matsuconfi@gmail.com>",
            ticket_free_text="Tämä on sähköinen lippusi Matsucon 2018 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
            "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Matsuconhin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Matsucon 2018 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://matsucon.fi'>Matsucon 2018 -tapahtuman kotisivuilta</a>.</p>",
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
                name="Viikonlopun lippu",
                description="Matsuconin pääsylippu, joka oikeuttaa pääsyn tapahtumaan molempina päivinä.",
                limit_groups=[
                    limit_group("Viikonloppuliput", 720),
                ],
                price_cents=1500,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Lauantain lippu",
                description="Matsuconin pääsylippu, joka oikeuttaa pääsyn tapahtumaan lauantaina.",
                limit_groups=[
                    limit_group("Lauantailiput", 120),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Sunnuntain lippu",
                description="Matsuconin pääsylippu, joka oikeuttaa pääsyn tapahtumaan sunnuntaina.",
                limit_groups=[
                    limit_group("Sunnuntailiput", 120),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Lattiamajoitus",
                description="Lattiamajoitus lauantain ja sunnuntain väliselle yölle tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Lattiamajoituspaikat", 40),
                ],
                price_cents=700,
                electronic_ticket=False,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Lattiamajoitus + aamiainen",
                description="Lattiamajoitus sekä aamiainen lauantain ja sunnuntain väliselle yölle tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Lattiamajoituspaikat", 40),
                ],
                price_cents=1000,
                electronic_ticket=False,
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


class Command(BaseCommand):
    args = ""
    help = "Setup matsucon2018 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
