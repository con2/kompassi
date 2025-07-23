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
        # self.setup_programme()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Hyvinkään villatehdas",
            defaults=dict(
                name_inessive="Hyvinkään villatehtaalla",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="hyvinkaan-nuorisopalvelut",
            defaults=dict(
                name="Hyvinkään nuorisopalvelut",
                name_genitive="Hyvinkään nuorisopalveluiden",
                homepage_url="http://www.hyvinkaa.fi/kulttuuri-ja-vapaa-aika/nuoriso/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="hypecon2020",
            defaults=dict(
                name="Hypecon ja Hypecon Encore (2020)",
                name_genitive="Hypeconin",
                name_illative="Hypeconiin",
                name_inessive="Hypeconssa",
                homepage_url="http://www.hypecon.net/",
                organization=self.organization,
                start_time=datetime(2020, 6, 6, 10, 0, tzinfo=self.tz),
                end_time=datetime(2020, 6, 7, 20, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_programme(self):
        from kompassi.core.utils import full_hours_between
        from kompassi.labour.models import PersonnelClass
        from kompassi.zombies.programme.models import (
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
            programme_event_meta.contact_email = "Hypecon <hypecon@hypecon.net>"
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
            ("Pelit", "rope"),
            ("Anime/manga", "anime"),
            ("Cosplay", "cosplay"),
            ("Muu", "muu"),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                ),
            )

        for tag_name, tag_style in [
            ("Luento", "label-default"),
            ("Paneeli", "label-success"),
            ("Keskustelupiiri", "label-info"),
            ("Työpaja", "label-warning"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
            )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time,
                    self.event.end_time,
                ),
            ]:
                TimeBlock.objects.get_or_create(
                    event=self.event, start_time=start_time, defaults=dict(end_time=end_time)
                )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 22:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
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
            work_begins=self.event.start_time.replace(hour=9, tzinfo=self.tz),
            work_ends=self.event.end_time,
            admin_group=labour_admin_group,
            contact_email="Hypecon <hypecon@hypecon.net>",
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
            # ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            # ('Media', 'media', 'badges'),
            # ('Myyjä', 'myyja', 'badges'),
            # ('Vieras', 'vieras', 'badges'),
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
        conitea = PersonnelClass.objects.get(event=self.event, slug="conitea")

        for name, description, pcs in [
            ("Conitea", "Tapahtuman järjestelytoimikunnan eli conitean jäsen", [conitea]),
            (
                "Järjestyksenvalvoja",
                "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa "
                "JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole "
                "täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
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
                signup_form_class_path="events.hypecon2020.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.hypecon2020.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('HYPEWORK', 'Työvoimawiki', 'accepted'),
            # ('HYPEINFO', 'Infowiki', 'info'),
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

        for team_slug, team_name in [
            ("pj", "Pääjärjestäjät"),
            ("ohjelma", "Ohjelma"),
            ("tuotanto", "Tuotanto"),
            ("talous", "Talous"),
            ("tiedotus", "Tiedotus"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = f"{team_slug}@hypecon.net"

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(name=team_name, order=self.get_ordering_number(), group=team_group, email=email),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup hypecon2020 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
