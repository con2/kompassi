from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone, now

from kompassi.core.models import Event, Organization, Person, Venue
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models import (
    AlternativeSignupForm,
    InfoLink,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
    Qualification,
)
from kompassi.program_v2.models.meta import ProgramV2EventMeta

from ...models import SignupExtra, SpecialDiet


class Setup:
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = get_current_timezone()
        self.setup_core()
        self.setup_labour()
        self.setup_program_v2()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        self.venue, unused = Venue.objects.get_or_create(
            name="Tampere-talo",
            defaults=dict(
                name_inessive="Tampere-talossa",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="tampere-kuplii-ry",
            defaults=dict(
                name="Tampere Kuplii ry",
                homepage_url="http://ry.tamperekuplii.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="kuplii2026",
            defaults=dict(
                name="Tampere Kuplii 2026",
                name_genitive="Tampere Kuplii 2026 -tapahtuman",
                name_illative="Tampere Kuplii 2026 -tapahtumaan",
                name_inessive="Tampere Kuplii 2026 -tapahtumassa",
                homepage_url="http://2026.tamperekuplii.fi",
                organization=self.organization,
                start_time=datetime(2026, 3, 28, 10, 0, tzinfo=self.tz),
                end_time=datetime(2026, 3, 29, 17, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Tampere Kupliin työvoimatiimi <tyovoima@tamperekuplii.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ("Kuplitea", "kuplitea", "labour"),
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
        PersonnelClass.objects.get(event=self.event, slug="kuplitea")

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="kuplii2025"),
                target_event=self.event,
            )

        for name in ["Kuplitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications.set([qual])

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
            slug="kuplitea",
            defaults=dict(
                title="Kuplitean ilmoittautumislomake",
                signup_form_class_path="events.kuplii2026.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.kuplii2026.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ("KUPLIIWORK", "Työvoimawiki", "accepted"),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=f"https://confluence.tracon.fi/display/{wiki_space}",
                    group=labour_event_meta.get_group(link_group),
                ),
            )

    def setup_program_v2(self):
        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Tampere Kupliin ohjelmatiimi <ohjelma@tamperekuplii.fi>",
                is_accepting_feedback=False,
                default_registry=Registry.objects.get_or_create(
                    scope=self.organization.scope,
                    slug="volunteers",
                    defaults=dict(
                        title_fi="Tampere Kuplii ry:n vapaaehtoisrekisteri",
                        title_en="Volunteers of Tampere Kuplii",
                    ),
                )[0],
            ),
        )
        meta.ensure()

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
        organizer_group = self.event.labour_event_meta.get_group("kuplitea")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("kuplitea", "Kuplitea"),
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
    help = "Setup kuplii2026 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
