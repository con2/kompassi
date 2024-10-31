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
        # ctora_team, created = Team.objects.get_or_create(
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
        from forms.models.meta import FormsEventMeta
        from forms.models.survey import Survey

        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])

        FormsEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

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
