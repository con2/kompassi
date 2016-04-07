from django.test import TestCase
from django.utils.timezone import now

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

from labour.models import Signup

from .utils import next_full_hour
from .models import ProgrammeEventMeta, ProgrammeRole


class UtilsTestCase(TestCase):
    def test_next_full_hour(self):
        tz = tzlocal()

        self.assertEqual(
          next_full_hour(datetime(2013, 8, 15, 19, 4, 25, tzinfo=tz)),
          datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz)
        )

        self.assertEqual(
          next_full_hour(datetime(2013, 8, 15, 14, 0, 0, tzinfo=tz)),
          datetime(2013, 8, 15, 14, 0, 0, tzinfo=tz)
        )

    def test_schedule_is_public(self):
        meta, unused = ProgrammeEventMeta.get_or_create_dummy()

        a_week_from_now = now() + timedelta(days=7)
        a_week_ago = now() - timedelta(days=7)

        meta.public_From = a_week_from_now
        assert not meta.is_public

        meta.public_from = a_week_ago
        assert meta.is_public

        meta.public_from = None
        assert not meta.is_public


class ProgrammeSignupExtraTestCase(TestCase):
    def test_condb_164_programme_to_labour_to_nothing(self):
        programme_role, unused = ProgrammeRole.get_or_create_dummy()
        programme = programme_role.programme
        person = programme_role.person
        event = programme.category.event
        SignupExtra = event.programme_event_meta.signup_extra_model
        assert SignupExtra.supports_programme

        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk is None
        signup_extra.save()

        programme.apply_state()
        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk is not None
        signup_extra_pk = signup_extra.pk
        assert signup_extra.is_active

        signup, created = Signup.get_or_create_dummy(accepted=True)
        signup.apply_state()
        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk == signup_extra_pk
        assert signup_extra.is_active

        programme.state = 'rejected'
        programme.save()
        programme.apply_state()
        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk == signup_extra_pk
        assert signup_extra.is_active

        signup.personnel_classes = []
        signup.job_categories_accepted = []
        signup.state = 'cancelled'
        assert not signup.is_active
        signup.save()
        signup.apply_state()
        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk == signup_extra_pk
        assert not signup_extra.is_active
