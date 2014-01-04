from django.test import TestCase

from datetime import datetime, timedelta

from dateutil.tz import tzlocal

from .utils import next_full_hour, full_hours_between


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