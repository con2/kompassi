# encoding: utf-8

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.forms import ValidationError
from django.test import TestCase

from dateutil.tz import tzlocal

from .utils import check_password_strength, full_hours_between, slugify


class UtilsTestCase(TestCase):
    def test_check_password_strength(self):
        check_password_strength('pieniISO6',
            min_length=8,
            min_classes=3,
        )

        check_password_strength('pieni6',
            min_length=6,
            min_classes=2,
        )

        try:
            check_password_strength('pieni6',
                min_length=8,
                min_classes=2,
            )
            assert False
        except ValidationError, e:
            pass

        try:
            check_password_strength('pieni6',
                min_length=6,
                min_classes=3,
            )
            assert False
        except ValidationError, e:
            pass

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
