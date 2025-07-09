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
        self.setup_badges()
        self.setup_tickets()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Kulttuuritalo (Helsinki)",
            defaults=dict(
                name_inessive="Kulttuuritalossa Helsingissä",
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
            slug="popcultday2018",
            defaults=dict(
                name="Popcult Day 2018",
                name_genitive="Popcult Day 2018 -tapahtuman",
                name_illative="Popcult Day 2018 -tapahtumaan",
                name_inessive="Popcult Day 2018 -tapahtumassa",
                homepage_url="http://popcult.fi/day-2018",
                organization=self.organization,
                start_time=datetime(2018, 5, 12, 10, 0, tzinfo=self.tz),
                end_time=datetime(2018, 5, 12, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Person
        from labour.models import (
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
            from core.models import Person

            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email="Popcult Helsingin työvoimavastaava <virve.honkala@popcult.fi>",
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        for jc_data in [
            ("Vastaava", "Tapahtuman järjestelytoimikunnan jäsen eli vastaava", [vastaava]),
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
                signup_form_class_path="events.popcultday2018.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.popcultday2018.forms:OrganizerSignupExtraForm",
                active_from=datetime(2018, 1, 21, 0, 0, 0, tzinfo=self.tz),
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
            reference_number_template="2018{:05d}",
            contact_email="Popcult Helsinki <liput@popcult.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Popcult Day 2018 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
            "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Popcult Dayhin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Popcult Day 2018 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://popcult.fi/day-2018'>Popcult Day 2018 -tapahtuman kotisivuilta</a>.</p>",
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
                name="Popcult Day 2018 -lippu",
                description="Yksi pääsylippu Popcult Day -tapahtumaan lauantaille 12.5.2018. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.",
                limit_groups=[
                    limit_group("Pääsyliput", 800),
                ],
                price_cents=1400,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Kahden lipun tarjouspaketti Popcult Dayhin 2018",
                override_electronic_ticket_title="Popcult Day 2018 -tarjouslippu",
                description="Kaksi pääsylippua Popcult Day -tapahtumaan lauantaille 12.5.2018. Osta liput edullisemmin itsellesi ja vaikka lahjaksi kaverille! Sisältää kaksi sähköistä lippua, jotka vaihdetaan rannekkeisiin tapahtumapaikalla. Rajoitettu tarjous, myynnissä su 18.2. klo 23:59 asti.",
                limit_groups=[
                    limit_group("Kahden lipun tarjouspaketit", 100),
                ],
                price_cents=2500,
                electronic_ticket=True,
                electronic_tickets_per_product=2,
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

        # v5
        if not meta.print_logo_path:
            meta.print_logo_path = mkpath("static", "images", "popcult.png")
            meta.print_logo_width_mm = 30
            meta.print_logo_height_mm = 30
            meta.save()


class Command(BaseCommand):
    args = ""
    help = "Setup popcultday2018 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
