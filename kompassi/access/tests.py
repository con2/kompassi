from unittest import TestCase as NonDatabaseTestCase

import pytest
from django.test import RequestFactory, TestCase

from kompassi.core.models import Person
from kompassi.core.models.event import Event
from kompassi.event_log_v2.models.entry import Entry
from kompassi.forms.models.survey import Survey
from kompassi.labour.models import LabourEventMeta

from .constants import CBAC_PERMISSION_DENIED, CBAC_SUDO_CLAIMS
from .exceptions import CBACPermissionDenied
from .models import CBACEntry, Claims, EmailAlias, EmailAliasType, GroupEmailAliasGrant
from .models.email_alias_type import EmailAliasVariant
from .sudo import grant_sudo
from .utils import emailify


class FakePerson:
    first_name = "Luka"
    surname = "Pajukanta"


class EmailifyTestCase(NonDatabaseTestCase):
    def test_emailify(self):
        assert emailify("") == ""
        assert emailify("Luka Pajukanta") == "luka.pajukanta"
        assert emailify("Kalle-Jooseppi Mäki-Kangas-Ketelä") == "kalle-jooseppi.maki-kangas-ketela"

    def test_firstname_surname(self):
        assert (
            EmailAliasVariant.FIRSTNAME_LASTNAME.get_account_name(
                FakePerson(),  # type: ignore
                None,  # type: ignore
            )
            == "luka.pajukanta"
        )


class EmailAliasesTestCase(TestCase):
    def setUp(self):
        self.meta, _unused = LabourEventMeta.get_or_create_dummy()
        self.group = self.meta.get_group("admins")
        self.person, _unused = Person.get_or_create_dummy()

    def test_email_alias_create(self):
        email_alias, _unused = EmailAlias.get_or_create_dummy()
        assert email_alias.email_address == "markku.mahtinen@example.com"

    def test_ensure_aliases(self):
        alias_type, _unused = EmailAliasType.get_or_create_dummy()

        self.group_grant, _unused = GroupEmailAliasGrant.objects.get_or_create(group=self.group, type=alias_type)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        assert alias_type.email_aliases.count() == 0

        self.person.user.groups.add(self.group)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        assert alias_type.email_aliases.count() == 1

    def test_account_name_generator_returning_none(self):
        alias_type, _unused = EmailAliasType.get_or_create_dummy(variant=EmailAliasVariant.NICK)

        self.person.nick = ""
        self.person.save()

        assert alias_type.email_aliases.count() == 0

        GroupEmailAliasGrant.ensure_aliases(self.person)

        assert alias_type.email_aliases.count() == 0


def get_claims(event: Event, app_name: str) -> Claims:
    return {
        "organization": event.organization.slug,
        "event": event.slug,
        "app": app_name,
        "view": "start_view",
        "method": "POST",
    }


@pytest.mark.django_db
def test_ensure_admin_group_privileges():
    """
    Given there is an event that uses the labour module
    And there is a person
    When that person is given labour admin privileges for the event
    Then they can perform labour admin actions in that event
    But they cannot perform programme admin actions in that event

    When that person is stripped of labour admin privileges for the event
    Then they cannot perform labour admin actions in that event
    And they cannot perform programme admin actions in that event
    """
    # TODO find out how to hook this up to pytest.mark.django_db
    Entry.ensure_partitions()

    meta, _unused = LabourEventMeta.get_or_create_dummy()
    event = meta.event
    person, _unused = Person.get_or_create_dummy()
    assert person.user

    meta.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges()

    assert CBACEntry.is_allowed(person.user, get_claims(event, "labour"))
    assert not CBACEntry.is_allowed(person.user, get_claims(event, "programme"))

    meta.admin_group.user_set.remove(person.user)
    CBACEntry.ensure_admin_group_privileges()

    assert not CBACEntry.is_allowed(person.user, get_claims(event, "labour"))
    assert not CBACEntry.is_allowed(person.user, get_claims(event, "programme"))


SURVEY_RESPONSES_QUERY = """
  query SurveyResponses($eventSlug: String!) {
    event(slug: $eventSlug) {
      forms {
        survey(slug: "test-survey") {
          responses {
            id
          }
        }
      }
    }
  }
"""


def _graphql_request(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    return request


@pytest.mark.django_db
def test_cbac_denial_does_not_leak_claims():
    """
    Regression test for the leak fixed in kompassi/access/exceptions.py:
    CBACPermissionDenied used to call a no-op `super()` and carry no extensions, so
    str(exc) was the repr of the claims dict and a denied caller received the internal
    app/model/field names in errors[0].message. A denial must now surface a generic
    message plus a machine-readable code, and (for a non-superuser) no claims.
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    Survey.objects.create(event=event, slug="test-survey")

    person, _created = Person.get_or_create_dummy(superuser=False)

    result = schema.execute(
        SURVEY_RESPONSES_QUERY,
        None,
        _graphql_request(person.user),
        variable_values=dict(eventSlug=event.slug),
    )

    assert result.errors
    assert len(result.errors) == 1
    error = result.errors[0]
    assert error.message == "Permission denied"
    assert error.extensions == {"code": CBAC_PERMISSION_DENIED}


@pytest.mark.django_db
def test_cbac_denial_exposes_claims_to_superuser():
    """
    A superuser gets the denied claims back (restricted to CBAC_SUDO_CLAIMS) so the
    frontend can offer the sudo override; a non-superuser never does (see above).
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    Survey.objects.create(event=event, slug="test-survey")

    person, _created = Person.get_or_create_dummy(superuser=True, another=True)

    result = schema.execute(
        SURVEY_RESPONSES_QUERY,
        None,
        _graphql_request(person.user),
        variable_values=dict(eventSlug=event.slug),
    )

    assert result.errors
    error = result.errors[0]
    assert error.extensions is not None
    assert error.extensions["code"] == CBAC_PERMISSION_DENIED
    claims = error.extensions["claims"]
    assert set(claims.keys()) <= set(CBAC_SUDO_CLAIMS)
    assert claims["organization"] == event.organization.slug
    assert claims["event"] == event.slug
    assert claims["app"] == "forms"


@pytest.mark.django_db
def test_grant_sudo_rejects_non_superuser():
    person, _created = Person.get_or_create_dummy(superuser=False)

    with pytest.raises(CBACPermissionDenied):
        grant_sudo(person.user, {"organization": "dummy-org"})


@pytest.mark.django_db
def test_grant_sudo_rejects_empty_claims():
    """
    CBACEntry.is_allowed uses claims__contained_by, under which a {} claims entry would
    match every possible permission. Sudo must never mint one, even if the caller's
    claims dict only contained keys outside CBAC_SUDO_CLAIMS.
    """
    person, _created = Person.get_or_create_dummy(superuser=True)

    with pytest.raises(ValueError):
        grant_sudo(person.user, {"view": "some_view", "method": "POST"})


@pytest.mark.django_db
def test_sudo_cbac_mutation_grants_temporary_access():
    """
    End to end: a query denied for a superuser succeeds after sudoCbac is called with
    the claims the denial exposed, and both audit events are emitted.
    """
    from kompassi.graphql_api.schema import schema

    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    Survey.objects.create(event=event, slug="test-survey")

    person, _created = Person.get_or_create_dummy(superuser=True, another=True)
    request = _graphql_request(person.user)

    denied = schema.execute(
        SURVEY_RESPONSES_QUERY,
        None,
        request,
        variable_values=dict(eventSlug=event.slug),
    )
    assert denied.errors
    claims = denied.errors[0].extensions["claims"]

    sudo_result = schema.execute(
        """
          mutation SudoCbac($input: SudoCbacInput!) {
            sudoCbac(input: $input) {
              validUntil
            }
          }
        """,
        None,
        request,
        variable_values=dict(input=dict(claims=claims)),
    )
    assert not sudo_result.errors
    assert sudo_result.data is not None
    assert sudo_result.data["sudoCbac"]["validUntil"]

    allowed = schema.execute(
        SURVEY_RESPONSES_QUERY,
        None,
        request,
        variable_values=dict(eventSlug=event.slug),
    )
    assert not allowed.errors

    assert Entry.objects.filter(entry_type="access.cbac.sudo").exists()
    assert Entry.objects.filter(entry_type="access.cbacentry.created").exists()
