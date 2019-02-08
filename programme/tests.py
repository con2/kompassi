from django.test import TestCase
from django.utils.timezone import now

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

from access.models import SlackAccess, GroupPrivilege, Privilege
from labour.models import Signup

from .utils import next_full_hour
from .models import ProgrammeEventMeta, ProgrammeRole, Programme, Room


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

        meta.public_from = a_week_from_now
        assert not meta.is_public

        meta.public_from = a_week_ago
        assert meta.is_public

        meta.public_from = None
        assert not meta.is_public


class ProgrammeSignupExtraTestCase(TestCase):
    def test_condb_164_programme_to_labour_to_nothing(self):
        """
        In this test a person first accepts an invitation as a speaker and enters their
        personal data (in a SignupExtra). Then they also sign up as a worker.

        However, they then cancel first their programme and then their worker signup. The
        SignupExtra should be marked inactive only after both are cancelled.
        """

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

        signup.personnel_classes.set([])
        signup.job_categories_accepted.set([])
        signup.state = 'cancelled'
        assert not signup.is_active
        signup.save()
        signup.apply_state()
        signup_extra = SignupExtra.for_event_and_person(event, person)
        assert signup_extra.pk == signup_extra_pk
        assert not signup_extra.is_active


class ProgrammeSlackAccessTestCase(TestCase):
    def test_condb_434_programme_slack_access(self):
        programme_role, unused = ProgrammeRole.get_or_create_dummy()
        programme = programme_role.programme
        person = programme_role.person
        event = programme.category.event
        meta = event.programme_event_meta
        group = meta.get_group('hosts')

        slack_access, unused = SlackAccess.get_or_create_dummy()
        privilege = slack_access.privilege
        group_privilege, unused = GroupPrivilege.objects.get_or_create(
            privilege=privilege,
            group=group,
            event=event,
        )

        assert person.user in group.user_set.all()
        assert privilege in Privilege.get_potential_privileges(person)

        programme.state = 'rejected'
        programme.save()
        programme.apply_state()

        group = meta.get_group('hosts')
        assert person.user not in group.user_set.all()
        assert privilege not in Privilege.get_potential_privileges(person)


class ProgrammeTestCase(TestCase):
    def test_programmes_without_end_time_showing_as_past(self):
        t = now()

        pr, unused = ProgrammeRole.get_or_create_dummy()

        programme = pr.programme
        programme.start_time = None
        programme.length = None
        programme.save()

        event = programme.category.event
        event.start_time = t - timedelta(days=20)
        event.end_time = t - timedelta(days=17)
        event.save()

        person = pr.person

        assert not Programme.get_future_programmes(person).exists()
        assert Programme.get_past_programmes(person).exists()
