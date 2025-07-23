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
        # self.setup_programme()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Tampereen yliopisto",
            defaults=dict(
                name_inessive="Tampereen yliopistolla",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="Finncon-yhdistys ry",
            defaults=dict(
                name="Finncon-yhdistys ry",
                homepage_url="http://www.finncon.org/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="finncon2023",
            defaults=dict(
                name="Finncon 2023",
                name_genitive="Finncon 2023 -tapahtuman",
                name_illative="Finncon 2023 -tapahtumaan",
                name_inessive="Finncon 2023 -tapahtumassa",
                homepage_url="http://2023.finncon.org",
                organization=self.organization,
                start_time=datetime(2023, 7, 7, 10, 0, tzinfo=self.tz),
                end_time=datetime(2023, 7, 9, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_programme(self):
        from kompassi.core.utils import full_hours_between
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

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = "Finnconin ohjelmavastaava <ohjelma@2023.finncon.org>"
            programme_event_meta.save()

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

        for category_name, category_style in [
            ("Suomi", "color2"),
            ("English", "color1"),
            ("Svenska", "color3"),
            ("Academic Program", "color5"),
            ("Peruttu", "color4"),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                ),
            )

        for tag_title, tag_class in [
            ("Kunniavieras/Guest of Honor", "hilight"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time,
                    self.event.start_time.replace(hour=22, tzinfo=self.tz),
                ),
                (
                    self.event.end_time.replace(hour=9, tzinfo=self.tz),
                    self.event.end_time,
                ),
            ]:
                TimeBlock.objects.get_or_create(
                    event=self.event, start_time=start_time, defaults=dict(end_time=end_time)
                )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

        default_form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa ohjelmaa",
                programme_form_code="events.finncon2023.forms:ProgrammeForm",
                num_extra_invites=3,
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
        )

        from ...models import SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            # TODO bogus dates
            work_begins=self.event.start_time.replace(hour=8),
            work_ends=self.event.start_time.replace(hour=22),
            admin_group=labour_admin_group,
            contact_email="Finnconin työvoimavastaava <tyovoima@2023.finncon.org>",
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
            ("Conitea", "conitea", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Kunniavieras", "goh", "badges"),
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
                source_event=Event.objects.get(slug="finncon2018"),
                target_event=self.event,
            )

        for name in ["Conitea"]:
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
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.finncon2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.finncon2023.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('FINNCON2023', 'Finnconin työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=f"https://confluence.tracon.fi/display/{wiki_space}",
                    group=labour_event_meta.get_group(link_group),
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

        for team_slug, team_name in [("conitea", "Conitea")]:
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
    help = "Setup finncon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
