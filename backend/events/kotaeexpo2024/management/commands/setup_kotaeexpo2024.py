from datetime import datetime, timedelta

import yaml
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from pkg_resources import resource_stream


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
        #        self.setup_programme()
        self.setup_intra()
        self.setup_access()
        self.setup_directory()
        self.setup_forms()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.organization, unused = Organization.objects.get_or_create(
            slug="kotae-ry",
            defaults=dict(
                name="Kotae ry",
                homepage_url="https://www.kotae.fi",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(name="Tampereen Messu- ja Urheilukeskus")
        self.event, unused = Event.objects.get_or_create(
            slug="kotaeexpo2024",
            defaults=dict(
                name="Kotae Expo (2024)",
                name_genitive="Kotae Expon",
                name_illative="Kotae Expoon",
                name_inessive="Kotae Expossa",
                homepage_url="http://www.kotae.fi",
                organization=self.organization,
                start_time=datetime(2024, 6, 29, 10, 0, tzinfo=self.tz),
                end_time=datetime(2024, 6, 30, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Survey,
        )

        from ...models import Accommodation, KnownLanguage, SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Kotae Expon vapaaehtoistiimi <vapaaehtoiset@kotae.fi>",
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

        for pc_name, pc_slug, pc_app_label, pc_afterparty in [
            ("Vastaava", "vastaava", "labour", True),
            ("Vapaaehtoinen", "vapaaehtoinen", "labour", True),
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

        vapaaehtoinen = PersonnelClass.objects.get(event=self.event, slug="vapaaehtoinen")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        for jc_data in [
            ("vastaava", "Vastaava", "Tapahtuman järjestelytoimikunnan jäsen", [vastaava]),
            (
                "yleinen",
                "Yleisvänkäri",
                "Olet conissa niinsanottu joka puun höylä, eli tarvittaessa olet kutsuttavissa auttamaan muita tiimejä erilaisissa tehtävissä, kuten mm. vesipisteiden täytössä tai ruuhka-ajan narikassa.",
                [vapaaehtoinen],
            ),
        ]:
            slug, name, description, pcs = jc_data

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    name=name,
                    description=description,
                ),
            )

            if created:
                job_category.personnel_classes.set(pcs)

        labour_event_meta.create_groups()

        for name in ["Vastaava"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        # for jc_name, qualification_name in [
        #     ("Järjestyksenvalvoja", "JV-kortti"),
        # ]:
        #     jc = JobCategory.objects.get(event=self.event, name=jc_name)
        #     qual = Qualification.objects.get(name=qualification_name)

        #     jc.required_qualifications.set([qual])

        for language in [
            "Suomi",
            "Ruotsi",
            "Englanti",
            "Japani",
            "Korea",
        ]:
            KnownLanguage.objects.get_or_create(name=language)

        for accommodation_name in [
            "Pe-la väliselle yölle",
            "La-su väliselle yölle",
        ]:
            Accommodation.objects.get_or_create(name=accommodation_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                title="Vastaavien ilmoittautumislomake",
                signup_form_class_path="events.kotaeexpo2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.kotaeexpo2024.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="erikoistehtava",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.kotaeexpo2024.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.kotaeexpo2024.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Kotae Expon vastaavista on ohjeistanut sinua ilmoittautumaan tällä lomakkeella. "
                ),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="tyovuorotoiveet",
            defaults=dict(
                title="Työvuorotoiveet",
                description=(
                    "Tässä vaiheessa voit vaikuttaa työvuoroihisi. Jos saavut tapahtumaan vasta sen alkamisen "
                    "jälkeen tai sinun täytyy lähteä ennen tapahtuman loppumista, kerro se tässä. Lisäksi jos "
                    "tiedät ettet ole käytettävissä tiettyihin aikoihin tapahtuman aikana tai haluat esimerkiksi "
                    "nähdä jonkun ohjelmanumeron, kerro siitäkin. Työvuorotoiveiden toteutumista täysin ei voida "
                    "taata."
                ),
                form_class_path="events.kotaeexpo2024.forms:ShiftWishesSurvey",
                active_from=now(),
                active_until=self.event.start_time - timedelta(days=60),
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=False,
            ),
        )

    def setup_access(self):
        from access.models import (
            EmailAliasType,
            GroupEmailAliasGrant,
        )

        cc_group = self.event.labour_event_meta.get_group("vastaava")

        for metavar in [
            "etunimi.sukunimi",
            "nick",
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name="kotae.fi", metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                ),
            )

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("vastaava")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("pj", "Pääjärjestäjä"),
            ("talous", "Talous"),
            ("turvallisuus", "Turvallisuus"),
            ("viestinta", "Viestintä ja markkinointi"),
            ("tilat", "Tilat"),
            ("kunniavieras", "Kunniavieras"),
            ("vapaaehtoiset", "Vapaaehtoiset"),
            ("tekniikka", "Tekniikka"),
            ("taltiointi", "Taltiointi"),
            ("ohjelma", "Ohjelma"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = f"{team_slug}@kotae.fi"

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                    email=email,
                ),
            )

        for team in Team.objects.filter(event=self.event):
            team.is_public = True
            team.save()

    def setup_directory(self):
        from directory.models import DirectoryAccessGroup

        labour_admin_group = self.event.labour_event_meta.get_group("admins")

        DirectoryAccessGroup.objects.get_or_create(
            organization=self.event.organization,
            group=labour_admin_group,
            active_from=now(),
            active_until=self.event.end_time + timedelta(days=30),
        )

    def setup_forms(self):
        from forms.models.dimension import DimensionDTO
        from forms.models.form import Form
        from forms.models.survey import Survey

        # Dance judge signup form

        with resource_stream("events.kotaeexpo2024", "forms/dance-judge-signup-fi.yml") as f:
            data = yaml.safe_load(f)

        dance_judge_signup_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="dance-judge-signup-fi",
            language="fi",
            defaults=data,
        )

        # TODO temporary for development
        if not created:
            for key, value in data.items():
                setattr(dance_judge_signup_fi, key, value)
            dance_judge_signup_fi.save()

        dance_judge_signup_survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="dance-judge-signup",
            defaults=dict(
                active_from=now(),
                key_fields=["name"],
            ),
        )

        dance_judge_signup_survey.languages.set([dance_judge_signup_fi])

        with resource_stream("events.kotaeexpo2024", "forms/dance-judge-signup-dimensions.yml") as f:
            data = yaml.safe_load(f)

        for dimension in data:
            DimensionDTO.model_validate(dimension).save(dance_judge_signup_survey)

        # Cosplay judge signup form

        with resource_stream("events.kotaeexpo2024", "forms/cosplay-judge-signup-fi.yml") as f:
            data = yaml.safe_load(f)

        cosplay_judge_signup_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="cosplay-judge-signup-fi",
            language="fi",
            defaults=data,
        )

        # TODO temporary for development
        if not created:
            for key, value in data.items():
                setattr(cosplay_judge_signup_fi, key, value)
            cosplay_judge_signup_fi.save()

        cosplay_judge_signup_survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="cosplay-judge-signup",
            defaults=dict(
                active_from=now(),
                key_fields=["name"],
            ),
        )

        cosplay_judge_signup_survey.languages.set([cosplay_judge_signup_fi])

        with resource_stream("events.kotaeexpo2024", "forms/cosplay-judge-signup-dimensions.yml") as f:
            data = yaml.safe_load(f)

        for dimension in data:
            DimensionDTO.model_validate(dimension).save(cosplay_judge_signup_survey)

        # CMV judge signup form

        with resource_stream("events.kotaeexpo2024", "forms/cmv-judge-signup-fi.yml") as f:
            data = yaml.safe_load(f)

        cmv_judge_signup_fi, created = Form.objects.get_or_create(
            event=self.event,
            slug="cmv-judge-signup-fi",
            language="fi",
            defaults=data,
        )

        # TODO temporary for development
        if not created:
            for key, value in data.items():
                setattr(cmv_judge_signup_fi, key, value)
            cmv_judge_signup_fi.save()

        cmv_judge_signup_survey, _ = Survey.objects.get_or_create(
            event=self.event,
            slug="cmv-judge-signup",
            defaults=dict(
                active_from=now(),
                key_fields=["name"],
            ),
        )

        cmv_judge_signup_survey.languages.set([cmv_judge_signup_fi])

        with resource_stream("events.kotaeexpo2024", "forms/cmv-judge-signup-dimensions.yml") as f:
            data = yaml.safe_load(f)

        for dimension in data:
            DimensionDTO.model_validate(dimension).save(cmv_judge_signup_survey)


class Command(BaseCommand):
    args = ""
    help = "Setup Kotae Expo 2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
