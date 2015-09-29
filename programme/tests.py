from django.test import TestCase
from django.utils.timezone import now

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

from .utils import next_full_hour
from .models import ProgrammeEventMeta


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
