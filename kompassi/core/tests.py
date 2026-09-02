import json
import logging
import re
from datetime import date, datetime

import pytest
from babel import Locale
from dateutil.tz import tzlocal
from django.conf import settings
from django.test import TestCase
from django.utils.timezone import get_current_timezone

from kompassi.core.utils.time_utils import format_date_range

from .utils import MAX_PASSWORD_LENGTH, format_interval, full_hours_between, slugify

_ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def _build_log_formatter(name: str):
    spec = dict(settings.LOGGING["formatters"][name])
    formatter_class = spec.pop("()")
    return formatter_class(**spec)


def _make_log_record(**extra):
    record = logging.LogRecord(
        name="kompassi.test",
        level=logging.WARNING,
        pathname=__file__,
        lineno=1,
        msg="test message",
        args=None,
        exc_info=None,
    )
    for key, value in extra.items():
        setattr(record, key, value)
    return record


class LoggingFormatterTestCase(TestCase):
    def test_json_formatter_includes_extra_fields(self):
        formatter = _build_log_formatter("json")
        rendered = json.loads(formatter.format(_make_log_record(total=5)))

        assert rendered["message"] == "test message"
        assert rendered["total"] == 5
        assert "event" not in rendered

    def test_human_formatter_includes_extra_fields(self):
        formatter = _build_log_formatter("human")
        rendered = _ANSI_ESCAPE.sub("", formatter.format(_make_log_record(total=5)))

        assert "test message" in rendered
        assert "total=5" in rendered

    def test_json_formatter_extra_event_field_does_not_clobber_message(self):
        formatter = _build_log_formatter("json")
        rendered = json.loads(formatter.format(_make_log_record(event="tracon2026")))

        assert rendered["message"] == "test message"
        assert rendered["event"] == "tracon2026"

    def test_human_formatter_extra_event_field_does_not_clobber_message(self):
        formatter = _build_log_formatter("human")
        rendered = _ANSI_ESCAPE.sub("", formatter.format(_make_log_record(event="tracon2026")))

        assert "test message" in rendered
        assert "event=" in rendered
        assert "tracon2026" in rendered


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
                lambda t: datetime(2013, 8, 16, 1, 0, 0, tzinfo=tz) <= t <= datetime(2013, 8, 16, 2, 0, 0, tzinfo=tz)
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


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The password limit cannot be unified between client and server with plain markup. "
        "zxcvbn and Django's max_length both count Unicode code points (len()), but the HTML "
        "maxlength attribute is counted by browsers in UTF-16 code units. For a password of "
        "exactly MAX_PASSWORD_LENGTH code points containing an astral character (e.g. an emoji), "
        "the server accepts it while the browser would block it one character early. Making the "
        "input honour the code-point limit requires a custom widget with JavaScript. Deferred: "
        "sign-in is moving to a third-party product, at which point this becomes its concern."
    ),
)
def test_password_maxlength_unified_with_zxcvbn_for_astral_characters():
    """The client-side input limit should accept exactly what zxcvbn/the server accepts."""
    from kompassi.core.forms import RegistrationForm

    rendered = str(RegistrationForm()["password"])
    match = re.search(r'maxlength="(\d+)"', rendered)
    assert match, "password field should render a maxlength attribute"
    browser_maxlength = int(match.group(1))

    # Exactly MAX_PASSWORD_LENGTH code points, one of which is an astral character.
    password = "a" * (MAX_PASSWORD_LENGTH - 1) + "😀"
    # zxcvbn and Django count code points, so the server accepts this password.
    assert len(password) == MAX_PASSWORD_LENGTH

    # Browsers count the maxlength attribute in UTF-16 code units (the emoji is 2 units),
    # so a browser honouring maxlength would refuse this otherwise-valid password.
    utf16_units = len(password.encode("utf-16-le")) // 2
    assert utf16_units <= browser_maxlength


@pytest.mark.django_db
def test_program_role_retention_policy_null_round_trip():
    """
    Person.program_role_retention_policy is the first nullable PostgresEnumField, and the
    first one exposed via a form. NULL, the member itself and the member name must all
    round-trip, and an empty string (what an empty form select submits) must become NULL.
    """
    from kompassi.core.models.enums import ProgramRoleRetentionPolicy
    from kompassi.core.models.person import Person

    person, _created = Person.get_or_create_dummy()

    assert person.program_role_retention_policy is None

    person.program_role_retention_policy = ProgramRoleRetentionPolicy.REMOVE
    person.save(update_fields=["program_role_retention_policy"])
    person.refresh_from_db()
    assert person.program_role_retention_policy == ProgramRoleRetentionPolicy.REMOVE

    person.program_role_retention_policy = "RETAIN"  # type: ignore[assignment]
    person.save(update_fields=["program_role_retention_policy"])
    person.refresh_from_db()
    assert person.program_role_retention_policy == ProgramRoleRetentionPolicy.RETAIN

    person.program_role_retention_policy = None
    person.save(update_fields=["program_role_retention_policy"])
    person.refresh_from_db()
    assert person.program_role_retention_policy is None


@pytest.mark.django_db
def test_person_form_program_role_retention_policy():
    """
    The V1 profile form's empty select option must save as NULL rather than the empty
    string, which is not a label of the native enum type.
    """
    from kompassi.core.forms import PersonForm
    from kompassi.core.models.enums import ProgramRoleRetentionPolicy
    from kompassi.core.models.person import Person

    person, _created = Person.get_or_create_dummy()

    def submit(value: str):
        form_data = {field: getattr(person, field) or "" for field in PersonForm.Meta.fields}
        form_data["birth_date"] = "1990-01-01"
        form_data["program_role_retention_policy"] = value

        form = PersonForm(form_data, instance=person)
        assert form.is_valid(), form.errors
        return form.save()

    assert submit("REMOVE").program_role_retention_policy == ProgramRoleRetentionPolicy.REMOVE
    assert submit("RETAIN").program_role_retention_policy == ProgramRoleRetentionPolicy.RETAIN
    assert submit("").program_role_retention_policy is None
