from datetime import datetime, timedelta

from django.forms import ValidationError
from django.test import TestCase

from babel import Locale
from dateutil.tz import tzlocal

from .utils import full_hours_between, slugify, format_interval


class PersonTestCase(TestCase):
    def test_normalized_phone_number(self):
        from core.models import Person

        p = Person(phone='0505551234')
        self.assertEqual(
            p.normalized_phone_number,
            '+358 50 5551234'
        )

        p = Person(phone='ööää')
        self.assertEqual(
            p.normalized_phone_number,
            'ööää'
        )


class UtilsTestCase(TestCase):
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

    def test_slugify(self):
        assert slugify('Matti Lundén') == 'matti-lunden'

    def test_format_interval(self):
        tz = tzlocal()
        locale = Locale('fi')

        d0 = datetime(2016, 4, 27, 21, 0, 0, tzinfo=tz)
        d1 = datetime(2016, 4, 27, 23, 0, 0, tzinfo=tz)
        d2 = datetime(2016, 4, 28, 1, 0, 0, tzinfo=tz)

        self.assertEqual(
            format_interval(d0, d1, locale=locale),
            'ke 27.4. klo 21.00–23.00'
        )

        self.assertEqual(
            format_interval(d0, d2, locale=locale),
            'ke 27.4. klo 21.00 – to 28.4. klo 1.00'
        )
