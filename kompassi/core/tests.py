from datetime import date, datetime

from babel import Locale
from dateutil.tz import tzlocal
from django.test import TestCase
from django.utils.timezone import get_current_timezone

from kompassi.core.utils.time_utils import format_date_range

from .utils import format_interval, full_hours_between, slugify


class PersonTestCase(TestCase):
    def test_normalized_phone_number(self):
        from kompassi.core.models import Person

        p = Person(phone="0505551234")
        assert p.normalized_phone_number == "+358 50 5551234"

        p = Person(phone="ööää")
        assert p.normalized_phone_number == "ööää"


class UtilsTestCase(TestCase):
    def test_full_hours_between(self):
        tz = tzlocal()

        # input not full hour
        self.assertRaises(
            ValueError,
            full_hours_between,
            datetime(2013, 8, 15, 19, 4, 25, tzinfo=tz),
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
        )

        # start > end
        self.assertRaises(
            ValueError,
            full_hours_between,
            datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz),
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
        )

        # valid cases
        assert full_hours_between(
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
        ) == [datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz)]
        assert full_hours_between(
            datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz),
            datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz),
        ) == [datetime(2013, 8, 15, 20, 0, 0, tzinfo=tz), datetime(2013, 8, 15, 21, 0, 0, tzinfo=tz)]
        assert full_hours_between(
            datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 1, 0, 0, tzinfo=tz),
        ) == [
            datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 0, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 1, 0, 0, tzinfo=tz),
        ]
        assert full_hours_between(
            datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 3, 0, 0, tzinfo=tz),
            unless=(
                lambda t: (datetime(2013, 8, 16, 1, 0, 0, tzinfo=tz) <= t <= datetime(2013, 8, 16, 2, 0, 0, tzinfo=tz))
            ),
        ) == [
            datetime(2013, 8, 15, 23, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 0, 0, 0, tzinfo=tz),
            datetime(2013, 8, 16, 3, 0, 0, tzinfo=tz),
        ]

    def test_slugify(self):
        assert slugify("Matti Lundén") == "matti-lunden"

    def test_format_date_range(self):
        # all events are assumed to be in the server timezone (EET/EEST) for now
        tz = get_current_timezone()

        def mkdt(*args, **kwargs) -> datetime:
            return datetime(*args, **kwargs, tzinfo=tz)

        examples = [
            # date
            # Y, M, D match
            (date(2021, 8, 29), date(2021, 8, 29), "29.8.2021"),
            # Y, M match, D differ
            (date(2021, 8, 29), date(2021, 8, 30), "29.–30.8.2021"),
            # Y match, M, D differ
            (date(2021, 8, 29), date(2021, 9, 2), "29.8.–2.9.2021"),
            # Y, M, D differ
            (date(2021, 8, 29), date(2022, 1, 3), "29.8.2021–3.1.2022"),
            # datetime
            # Y, M, D match
            (mkdt(2021, 8, 29, 8, 0, 0), mkdt(2021, 8, 29, 18, 0, 0), "29.8.2021"),
            # Y, M match, D differ
            (mkdt(2021, 8, 29, 8, 0, 0), mkdt(2021, 8, 30, 18, 0, 0), "29.–30.8.2021"),
            # Y match, M, D differ
            (mkdt(2021, 8, 29, 8, 0, 0), mkdt(2021, 9, 2, 18, 0, 0), "29.8.–2.9.2021"),
            # Y, M, D differ
            (
                mkdt(2021, 8, 29, 8, 0, 0),
                mkdt(2022, 1, 3, 18, 0, 0),
                "29.8.2021–3.1.2022",
            ),
            # special case: first second considered to be the end of the previous day
            (mkdt(2021, 8, 29, 8, 0, 0), mkdt(2021, 8, 30, 0, 0, 0), "29.8.2021"),
        ]

        for start_date, end_date, expected in examples:
            actual = format_date_range(start_date, end_date)
            assert actual == expected

    def test_format_interval(self):
        tz = tzlocal()
        locale = Locale("fi")

        d0 = datetime(2016, 4, 27, 21, 0, 0, tzinfo=tz)
        d1 = datetime(2016, 4, 27, 23, 0, 0, tzinfo=tz)
        d2 = datetime(2016, 4, 28, 1, 0, 0, tzinfo=tz)

        assert format_interval(d0, d1, locale=locale) == "ke 27.4. 21.00–23.00"

        assert format_interval(d0, d2, locale=locale) == "ke 27.4. 21.00 – to 28.4. 1.00"
