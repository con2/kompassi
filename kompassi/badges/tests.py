import logging

import pytest
from django.db import transaction
from django.test import TestCase

from kompassi.core.models import Person
from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.dimension_value_dto import DimensionValueDTO
from kompassi.forms.models.form import Form
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey
from kompassi.labour.models import JobCategory, LabourEventMeta, PersonnelClass, Signup

from .models.badge import Badge
from .models.badges_event_meta import BadgesEventMeta
from .models.batch import Batch
from .models.survey_to_badge import SurveyToBadgeMapping

logger = logging.getLogger(__name__)


class BadgesTestCase(TestCase):
    def setUp(self):
        self.meta, unused = BadgesEventMeta.get_or_create_dummy()
        LabourEventMeta.get_or_create_dummy()

        self.event = self.meta.event
        self.person, unused = Person.get_or_create_dummy()

    def test_condb_423(self):
        """
        Even though a worker has requested to only show their nick or first name on their badge,
        some events have decided that the real name must always be visible.

        We assume this setting is not changed midway. If it is, all badges must be revoked.
        """
        self.person.preferred_name_display_style = "firstname_nick_lastname"
        self.person.preferred_badge_name_display_style = "nick"
        self.person.save()

        signup, unused = Signup.get_or_create_dummy(accepted=True)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert not badge.is_first_name_visible
        assert not badge.is_surname_visible

        self.meta.real_name_must_be_visible = True
        self.meta.save()

        badge.revoke()

        signup = Signup.objects.get(id=signup.id)
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.is_first_name_visible
        assert badge.is_surname_visible

    def test_condb_424(self):
        """
        If the job title of the worker changes while the badge has not been printed yet, the change
        should be reflected in the badge.
        """

        signup, unused = Signup.get_or_create_dummy(accepted=True)

        # No explicit job title
        signup.job_title = ""
        signup.save()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created

        jc1 = signup.job_categories_accepted.first()
        assert jc1
        assert badge.job_title == jc1.name

        jc2, unused = JobCategory.get_or_create_dummy(name="Hitman")
        signup.job_categories_accepted.set([jc2])
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.job_title == jc2.name

        # Explicit job title should override
        title = "Chief Hitman Commander to the Queen"
        signup.job_title = title
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.job_title == title

        # Removing explicit job title should reset to job category based title
        signup.job_title = ""
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.job_title == jc2.name

    def test_condb_429(self):
        """
        If a badge is revoked before it is printed or assigned into a batch, there is no need to
        leave it around revoked, it can be removed altogether.

        In this test, we arbitrarily revoke the badge of a worker who is still signed up to the event.
        Thus calling Badge.ensure again will re-create (or un-revoke) their badge.
        """
        signup, unused = Signup.get_or_create_dummy(accepted=True)
        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert not badge.is_printed

        badge = badge.revoke()

        assert badge is None
        assert not Badge.objects.filter(person=self.person, personnel_class__event=self.event).exists()

        badge, created = Badge.ensure(person=self.person, event=self.event)

        assert badge
        assert created

        batch = Batch.create(event=self.event)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.batch == batch
        assert not badge.is_printed

        badge = badge.revoke()
        assert badge is not None
        assert badge.is_revoked

        badge = Badge.objects.get(person=self.person, personnel_class__event=self.event)
        assert badge
        assert not created
        assert badge.is_revoked

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert created
        assert not badge.is_revoked

    def test_condb_137_intra_labour(self):
        """
        If the personnel class of the worker changes, the badge shall be revoked and a new one issued.
        """

        signup, unused = Signup.get_or_create_dummy(accepted=True)
        pc1 = signup.personnel_classes.get()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.personnel_class == pc1

        # Create another personnel class that is guaranteed to be higher in priority than the current one.
        pc2, unused = PersonnelClass.get_or_create_dummy(name="Sehr Wichtig Fellow", priority=pc1.priority - 10)

        self.event.labour_event_meta.create_groups()

        signup.personnel_classes.add(pc2)
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.personnel_class == pc2

    def test_condb_428_labour(self):
        """
        If someone is first accepted as a worker, but then cancels their participation or they are fired,
        their badge should get revoked.
        """
        signup, created = Signup.get_or_create_dummy(accepted=True)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert badge
        assert not created
        assert badge.personnel_class == signup.personnel_classes.get()

        # Now cancel the worker signup and make sure they go back to having a programme badge
        signup.personnel_classes.set([])
        signup.job_categories_accepted.set([])
        signup.state = "cancelled"
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge is None


@pytest.mark.django_db
def test_survey_to_badge():
    """
    Test the SurveyToBadgeMapping model and its match method.
    """
    BadgesEventMeta.get_or_create_dummy()
    FormsEventMeta.get_or_create_dummy()
    personnel_class, _ = PersonnelClass.get_or_create_dummy()
    event = personnel_class.event

    survey = Survey.objects.create(
        event=event,
        slug="test-survey",
        anonymity="NAME_AND_EMAIL",
    )

    DimensionDTO(
        slug="status",
        title={"en": "Status"},
        choices=[
            DimensionValueDTO(slug="new", title={"en": "New"}),
            DimensionValueDTO(slug="accepted", title={"en": "Accepted"}),
            DimensionValueDTO(slug="cancelled", title={"en": "New"}),
        ],
    ).save(survey.universe)

    survey.set_default_response_dimension_values({"status": ["new"]}, cache=survey.universe.preload_dimensions())

    form_en = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[],
    )

    SurveyToBadgeMapping.objects.create(
        survey=survey,
        personnel_class=personnel_class,
        required_dimensions={"status": ["accepted"]},
        job_title="Ohjelmanjärjestäjä",
    )

    person, _ = Person.get_or_create_dummy()

    with transaction.atomic():
        response = Response.objects.create(
            form=form_en,
            form_data={},
            revision_created_by=person.user,
        )
        survey.workflow.handle_new_response_phase1(response)
    survey.workflow.handle_new_response_phase2(response)

    assert not Badge.objects.filter(person=person, personnel_class__event=event).exists()

    with transaction.atomic():
        response.set_dimension_values({"status": ["accepted"]}, cache=survey.universe.preload_dimensions())
        response.refresh_cached_fields()
    survey.workflow.handle_response_dimension_update(response)

    badge = Badge.objects.filter(person=person, personnel_class__event=event).get()
    assert badge.personnel_class == personnel_class
    assert badge.job_title == "Ohjelmanjärjestäjä"
