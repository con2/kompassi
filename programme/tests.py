from django.test import TestCase
from django.utils.timezone import now

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

from .utils import next_full_hour, full_hours_between
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

    def test_full_hours_between(self):
        tz = tzlocal()

        # input not full hour
        self.assertRaises(
            ValueError,
            full_hours_between,
            datetime(2013, 8, 15, 19, 4, 25, tzinfo=tz),
            datetime(2013, 8, 15, 20, 0, 0,  tzinfo=tz)
        )

        # start > end
        self.assertRaises(
            ValueError,
            full_hours_between,
            datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz),
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz)
        )

        # valid cases
        self.assertEqual(
            full_hours_between(
                datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
                datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz)
            ),
            [
                datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz)
            ]
        )
        self.assertEqual(
            full_hours_between(
                datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
                datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz)
            ),
            [
                datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
                datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz)
            ]
        )
        self.assertEqual(
            full_hours_between(
                datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 1,  0, 0, tzinfo=tz)
            ),
            [
                datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 0,  0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 1,  0, 0, tzinfo=tz)
            ]
        )
        self.assertEqual(
            full_hours_between(
                datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 3,  0, 0, tzinfo=tz),
                unless=lambda t:
                  datetime(2013, 8, 16, 1,  0, 0, tzinfo=tz) <=
                  t <=
                  datetime(2013, 8, 16, 2,  0, 0, tzinfo=tz)
            ),
            [
                datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 0,  0, 0, tzinfo=tz),
                datetime(2013, 8, 16, 3,  0, 0, tzinfo=tz)
            ]
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
