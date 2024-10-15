import os
from datetime import datetime, timedelta

import yaml
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils.pkg_resources_compat import resource_stream


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
        # self.setup_programme()
        # self.setup_badges()
        # self.setup_tickets()
        self.setup_intra()
        self.setup_forms()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, _ = Venue.objects.get_or_create(
            name="SeAMK Frami F",
            defaults=dict(
                name_inessive="SeAMK Frami F:llä",
            ),
        )
        self.organization, _ = Organization.objects.get_or_create(
            slug="cosmocon-ry",
            defaults=dict(
                name="Cosmocon ry",
                homepage_url="https://cosmocon.fi/",
            ),
        )
        self.event, _ = Event.objects.get_or_create(
            slug="cosmocon2025",
            defaults=dict(
                name="Cosmocon 2025",
                name_genitive="Cosmoconin",
                name_illative="Cosmoconiin",
                name_inessive="Cosmoconissa",
                homepage_url="https://cosmocon.fi",
                organization=self.organization,
                start_time=datetime(2025, 2, 8, 11, 0, tzinfo=self.tz),
                end_time=datetime(2025, 2, 9, 17, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Person
        from labour.models import LabourEventMeta
        from labour.models.job_category import JobCategory
        from labour.models.personnel_class import PersonnelClass

        from ...models import SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from core.models import Person

            person, _ = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            registration_opens=datetime(2024, 10, 21, 0, 0, tzinfo=self.tz),
            registration_closes=self.event.start_time,
            admin_group=labour_admin_group,
            contact_email="Cosmoconin työvoimavastaava <talkoo@cosmocon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, _ = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        #
        # Personnel Classes - Henkilöstöluokat
        #

        # For reference:
        # ("Conitea", "coniitti", "labour"),
        # ("Työvoima", "tyovoima", "labour"),
        # ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
        # ("Guest of Honour", "goh", "badges"),
        # ("Media", "media", "badges"),
        # ("Myyjä", "myyja", "badges"),
        # ("Vieras", "vieras", "badges"),

        ## Organizers PersonnelClass
        organizers_personnel_class, _ = PersonnelClass.objects.get_or_create(
            event=self.event,
            slug="organizers",
            defaults=dict(
                name="Vastaavat",
                app_label="labour",
                priority=self.get_ordering_number(),
            ),
        )

        ## Volunteers PersonnelClass
        # volunteers_personnel_class, _ = PersonnelClass.objects.get_or_create(
        #     event=self.event,
        #     slug="volunteers",
        #     defaults=dict(
        #         name="Vapaaehtoiset",
        #         app_label="labour",
        #         priority=self.get_ordering_number(),
        #     ),
        # )

        #
        # Job categories - Tehtäväalueet
        #

        ## Cosmocon työryhmä JobCategory
        ctora_job_category, created = JobCategory.objects.get_or_create(
            event=self.event,
            slug="ctora",
            defaults=dict(
                name="Cosmocon työryhmä",
                description="Tapahtuman suunnittelusta ja valmistelusta vastaavan järjestelytyöryhmän jäsen",
                public=True,
            ),
        )
        if created:
            ctora_job_category.personnel_classes.set([organizers_personnel_class])

        ## Vapaaehtoiset JobCategory
        # staff_job_category, created = JobCategory.objects.get_or_create(
        #     event=self.event,
        #     slug="volunteer",
        #     defaults=dict(
        #         name="Vapaaehtoistyöntekijä",
        #         description="Järjestää tapahtumaa vapaaehtoisena talkootyöntekijänä",
        #     ),
        # )
        # if created:
        #     staff_job_category.personnel_classes.set([volunteers_personnel_class])

        ## Järjestyksenvalvoja JobCategory
        # jv_job_category, created = JobCategory.objects.get_or_create(
        #     event=self.event,
        #     slug="jv",
        #     defaults=dict(
        #         name="Järjestyksenvalvoja",
        #         description="Järjestyksenvalvojan tehtäviin kuuluvat lippujen tarkistus, kulunvalvonta sekä ihmisten ohjaus. Tehtävään vaaditaan JV-kortti. Syötä JV-kortin numero ja voimassaolotiedot oman Kompassiprofiilisi pätevyystietoihin ennen lomakkeen täyttämistä.",
        #     ),
        # )
        # if created:
        #     jv_job_category.personnel_classes.set([volunteers_personnel_class])
        #     jv_kortti_qualification = Qualification.objects.get(name="JV-kortti")
        #     jv_job_category.required_qualifications.set([jv_kortti_qualification])

        labour_event_meta.create_groups()

        # AlternativeSignupForm.objects.get_or_create(
        #    event=self.event,
        #    slug="conitea",
        #    defaults=dict(
        #        title="Conitean ilmoittautumislomake",
        #        signup_form_class_path="events.cosmocon2025.forms:OrganizerSignupForm",
        #        signup_extra_form_class_path="events.cosmocon2025.forms:OrganizerSignupExtraForm",
        #        active_from=now(),
        #        active_until=self.event.start_time,
        #    ),
        # )

    # def setup_badges(self):
    #     from badges.models import BadgesEventMeta
    #     (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
    #     meta, _ = BadgesEventMeta.objects.get_or_create(
    #         event=self.event,
    #         defaults=dict(
    #             admin_group=badge_admin_group,
    #         ),
    #     )

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import Category, ProgrammeEventMeta, Role, SpecialStartTime, TimeBlock

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, _ = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Cosmoconin ohjelmavastaava <ohjelma@cosmocon.fi>",
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
            reference_number_template="2025{:06d}",
            contact_email="Cosmocon <info@cosmocon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Cosmocon 2025 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
            "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
            "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
            "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
            "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
            "Tervetuloa Cosmoconiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Cosmocon 2025 -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='https://cosmocon.fi'>Cosmocon 2025 -tapahtuman kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, _ = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, _ = LimitGroup.objects.get_or_create(
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
                description="Viikonloppulippu oikeuttaa sisäänpääsyn molempiin Cosmoconin päiviin. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Viikonloppuliput", 650),
                ],
                price_cents=2000,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Lauantailippu",
                description="Lauantailippu oikeuttaa sisäänpääsyyn Cosmoconin ensimmäiseen päivään. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Lauantailiput", 200),
                ],
                price_cents=1500,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            dict(
                name="Sunnuntailippu",
                description="Sunnuntailippu oikeuttaa sisäänpääsyyn Cosmoconin toiseen päivään. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                limit_groups=[
                    limit_group("Sunnuntailiput", 150),
                ],
                price_cents=1500,
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

            product, _ = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)

    def setup_intra(self):
        from intra.models import IntraEventMeta
        # from intra.models.team import Team

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("ctora")
        meta, _ = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        # (ctora_intra_group,) = IntraEventMeta.get_or_create_groups(self.event, ["ctora"])
        # ctora_team_team, created = Team.objects.get_or_create(
        #     event=self.event,
        #     slug="ctora",
        #     defaults=dict(
        #         name="Cosmocon työryhmä",
        #         order=self.get_ordering_number(),
        #         group=ctora_intra_group,
        #     ),
        # )

    def setup_forms(self):
        from forms.models.dimension import DimensionDTO
        from forms.models.form import Form
        from forms.models.survey import Survey

        # Artist Alley application

        ## Artist Alley application - FI

        with resource_stream("events.cosmocon2025", "forms/artist-alley-application-fi.yml") as f:
            data = yaml.safe_load(f)

        artist_alley_application_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="artist-alley-application-fi",
            language="fi",
            defaults=data,
        )

        ## Artist Alley application - EN

        # with resource_stream("events.cosmocon2025", "forms/artist-alley-application-en.yml") as f:
        #     data = yaml.safe_load(f)

        # artist_alley_application_en, created = Form.objects.get_or_create(
        #     event=self.event,
        #     slug="artist-alley-application-en",
        #     language="en",
        #     defaults=data,
        # )

        artist_alley_application, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="artist-alley-application",
            defaults=dict(
                active_from=datetime(2024, 10, 21, 0, 0, tzinfo=self.tz),
                active_until=datetime(2024, 11, 8, 0, 0, tzinfo=self.tz),
                max_responses_per_user=1,
                key_fields=["name", "email", "day", "reserve"],
                login_required=True,
            ),
        )

        # artist_alley_application.languages.set([artist_alley_application_fi, artist_alley_application_en])
        artist_alley_application.languages.set([artist_alley_application_fi])

        with resource_stream("events.cosmocon2025", "forms/artist-alley-application-dimensions.yml") as f:
            artist_alley_dimensions = yaml.safe_load(f)
        for dimension in artist_alley_dimensions:
            DimensionDTO.model_validate(dimension).save(artist_alley_application)


class Command(BaseCommand):
    args = ""
    help = "Setup Cosmocon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
