import logging
import os
from datetime import datetime, timedelta

import yaml
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils.pkg_resources_compat import resource_stream

logger = logging.getLogger("kompassi")


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


class Setup:
    def __init__(self):
        self._ordering = 0
        self.dev_tickets = False

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False, dev_tickets: bool = False):
        self.test = test
        self.tz = tzlocal()
        self.dev_tickets = dev_tickets
        self.setup_core()
        self.setup_labour()
        # self.setup_programme()
        # self.setup_badges()
        # self.setup_tickets()
        self.setup_tickets_v2()
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
            labour_admin_group.user_set.add(person.user)  # type: ignore

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
                ticket_sales_starts=t - timedelta(days=60),  # type: ignore
                ticket_sales_ends=t + timedelta(days=60),  # type: ignore
            )

        meta, _ = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, _ = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )
            return limit_group

        viikonloppulippu, _ = Product.objects.get_or_create(
            event=self.event,
            name="LA+SU-lippu",
            defaults=dict(
                description="LA+SU-lippu oikeuttaa sisäänpääsyyn molempina tapahtumapäivinä 8-9.2.2025. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                price_cents=1500,
                electronic_ticket=True,
                available=True,
                ordering=10,
            ),
        )
        if not viikonloppulippu.limit_groups.exists():
            viikonloppulippu.limit_groups.set([limit_group("Viikonloppuliput", 275)])

        lauantailippu, _ = Product.objects.get_or_create(
            event=self.event,
            name="LA-lippu",
            defaults=dict(
                description="LA-lippu oikeuttaa sisäänpääsyyn lauantaina 8.2.2025. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=20,
            ),
        )
        if not lauantailippu.limit_groups.exists():
            lauantailippu.limit_groups.set([limit_group("Lauantailiput", 285)])

        sunnuntailippu, _ = Product.objects.get_or_create(
            event=self.event,
            name="SU-lippu",
            defaults=dict(
                description="SU-lippu oikeuttaa sisäänpääsyyn sunnuntaina 9.2.2025. Sähköinen lippu vaihdetaan ovella rannekkeeseen.",
                price_cents=800,
                electronic_ticket=True,
                available=True,
                ordering=30,
            ),
        )
        if not sunnuntailippu.limit_groups.exists():
            sunnuntailippu.limit_groups.set([limit_group("Sunnuntailiput", 285)])

    def setup_tickets_v2(self):
        if self.dev_tickets:
            logger.warning("--dev-tickets mode active! Tickets have zero price and no payment provider is configured.")

        from decimal import Decimal

        from tickets_v2.models.meta import TicketsV2EventMeta
        from tickets_v2.models.quota import Quota
        from tickets_v2.optimized_server.models.enums import PaymentProvider

        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                provider_id=PaymentProvider.NONE if self.dev_tickets else PaymentProvider.PAYTRAIL.value,
                terms_and_conditions_url_fi="https://cosmocon.fi/liput/toimitusehdot/",
            ),
        )
        meta.ensure_partitions()

        if Quota.objects.filter(event=self.event).exists():
            return

        def get_or_create_quota(name, amount) -> Quota:
            quota, created = Quota.objects.get_or_create(
                event=self.event,
                name=name,
            )
            quota.full_clean()
            if created:
                quota.set_quota(amount)
            quota.full_clean()
            return quota

        two_day_ticket_quota: Quota = get_or_create_quota("LA+SU-liput", 275)
        saturday_ticket_quota: Quota = get_or_create_quota("LA-liput", 285)
        sunday_ticket_quota: Quota = get_or_create_quota("SU-liput", 285)

        if self.test or self.dev_tickets:
            available_from = now()
            available_until = now() + timedelta(days=1)
        else:
            available_from = datetime(2024, 12, 5, 0, 0, tzinfo=self.tz)  # FIXME
            available_until = datetime(2025, 2, 8, 0, 0, tzinfo=self.tz)

        two_day_ticket_quota.products.get_or_create(
            event=self.event,
            title="Cosmocon (2025) - LA+SU",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("15.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        two_day_ticket_quota.full_clean()

        saturday_ticket_quota.products.get_or_create(
            event=self.event,
            title="Cosmocon (2025) - LA",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("10.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        saturday_ticket_quota.full_clean()

        sunday_ticket_quota.products.get_or_create(
            event=self.event,
            title="Cosmocon (2025) - SU",
            defaults=dict(
                price=Decimal("0.00") if self.dev_tickets else Decimal("8.00"),
                available_from=available_from,
                available_until=available_until,
            ),
        )
        sunday_ticket_quota.full_clean()

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
        from dimensions.models.dimension_dto import DimensionDTO
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

        with resource_stream("events.cosmocon2025", "forms/artist-alley-application-fi.yml") as f:
            data = yaml.safe_load(f)

        artist_alley_application_fi, created = Form.objects.get_or_create(
            event=self.event,
            survey=artist_alley_application,
            language="fi",
            defaults=data,
        )

        with resource_stream("events.cosmocon2025", "forms/artist-alley-application-dimensions.yml") as f:
            artist_alley_dimensions = yaml.safe_load(f)
        for dimension in artist_alley_dimensions:
            DimensionDTO.model_validate(dimension).save(artist_alley_application.universe)

        # Cosplay competition application
        cosplay_competition_application, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="cosplay-competition-application",
            defaults=dict(
                active_from=datetime(2024, 11, 1, 0, 0, tzinfo=self.tz),
                active_until=datetime(2024, 12, 16, 0, 0, tzinfo=self.tz),
                max_responses_per_user=1,
                key_fields=["name", "email", "character", "reserve"],
                login_required=True,
            ),
        )

        with resource_stream("events.cosmocon2025", "forms/cosplay-competition-application-fi.yml") as f:
            data = yaml.safe_load(f)

        cosplay_competition_application_fi, created = Form.objects.get_or_create(
            event=self.event,
            survey=cosplay_competition_application,
            language="fi",
            defaults=data,
        )

        with resource_stream("events.cosmocon2025", "forms/cosplay-competition-application-dimensions.yml") as f:
            cosplay_competition_dimensions = yaml.safe_load(f)
        for dimension in cosplay_competition_dimensions:
            DimensionDTO.model_validate(dimension).save(cosplay_competition_application.universe)


class Command(BaseCommand):
    args = ""
    help = "Setup Cosmocon2025 specific stuff"

    def add_arguments(self, parser):
        parser.add_argument("--dev-tickets", action="store_true", default=False)

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG, dev_tickets=opts["dev_tickets"])
