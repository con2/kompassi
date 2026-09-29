import pytest
from django.db import connection

from kompassi.core.models import Event, Person
from kompassi.core.pseudonymization import (
    REDACTED,
    find_orphan_tables,
    find_stale_classifications,
    find_unclassified_fields,
    pseudonymize,
    pseudonymize_form_data,
)
from kompassi.forms.models.form import Form
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey


def test_every_suspicious_field_is_classified():
    """
    A field that may hold personal data needs a rule in RULES or an entry in NOT_PERSONAL.
    `python manage.py pseudonymize_db --check` lists the fields that need one.
    """
    assert find_unclassified_fields() == []


def test_no_classification_names_a_missing_field():
    assert find_stale_classifications() == []


def test_pseudonymize_form_data():
    fields = [
        dict(slug="name", type="SingleLineText"),
        dict(slug="empty", type="SingleLineText"),
        dict(slug="shirt", type="SingleSelect"),
        dict(slug="days", type="MultiSelect"),
        dict(slug="birthday", type="DateField"),
        dict(slug="photo", type="FileUpload"),
        dict(slug="hetu", type="SingleLineText", encryptTo=["someone"]),
    ]
    form_data = {
        "name": "Markku Mahtinen",
        "empty": "",
        "shirt": "xl",
        "days.friday": "on",
        "birthday": "1984-01-01",
        "photo": ["https://example.com/photo.jpg"],
        "hetu": "eyJhbGciOi...",
        # answer to a field that has since been removed from the form
        "phone": "+358501234567",
    }

    assert pseudonymize_form_data(fields, form_data) == {
        "name": REDACTED,
        "empty": "",
        "shirt": "xl",
        "days.friday": "on",
    }


@pytest.mark.django_db
def test_pseudonymize():
    """
    Runs every rule against a database that has a little data in it, so that each rule's SQL
    gets executed at least once.
    """
    person, _ = Person.get_or_create_dummy()
    event, _ = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="pseudonymize-survey")
    form = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[dict(slug="name", type="SingleLineText", isKeyField=True)],
    )
    survey.refresh_cached_key_fields(form)
    response = Response.objects.create(form=form, form_data={"name": "Markku"}, ip_address="192.0.2.1")
    response.refresh_cached_fields()
    with connection.cursor() as cursor:
        # left behind by an app that has since been removed
        cursor.execute("CREATE TABLE sms_smsmessageout (id serial PRIMARY KEY, message text)")

    list(pseudonymize())

    assert find_orphan_tables() == []

    person.refresh_from_db()
    assert person.first_name == f"Person{person.pk}"
    assert person.email == f"person{person.pk}@example.com"
    assert person.birth_date.month == person.birth_date.day == 1

    user = person.user
    assert user
    user.refresh_from_db()
    assert user.username == f"user{user.pk}"
    assert user.email == person.email
    assert not user.has_usable_password()

    response.refresh_from_db()
    assert response.form_data == {"name": REDACTED}
    assert response.cached_key_fields == {"name": REDACTED}
    assert response.ip_address == ""
