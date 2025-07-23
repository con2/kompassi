import pytest
from django.test import TestCase
from jsonschema import ValidationError

from kompassi.zombies.programme.models import Programme, ProgrammeFeedback

from .models import Desuprofile, DesuprogrammeFeedback


class DesuprofileValidationTestCase(TestCase):
    def test_idempotence(self):
        valid_profile = dict(
            id=2559,
            username="japsu",
            email="foo@bar.fi",  # required
            first_name="Foo",
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date="2014-04-24",
        )

        assert Desuprofile.from_dict(valid_profile)._asdict() == valid_profile

    def test_desuprofile_without_required_attributes(self):
        blank_email = dict(
            id=2559,
            username="japsu",
            email="",  # required
            first_name="Foo",
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date="2014-04-24",
        )

        with pytest.raises(ValidationError):
            Desuprofile.from_dict(blank_email)

        missing_first_name = dict(
            id=2559,
            username="japsu",
            email="foo@bar.fi",
            # first_name='Foo',
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date="2014-04-24",
        )

        with pytest.raises(ValidationError):
            Desuprofile.from_dict(missing_first_name)

    def test_invalid_values(self):
        malformed_birth_date = dict(
            id=2559,
            username="japsu",
            email="foo@bar.fi",
            first_name="Foo",
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date="2014-04b-24",
        )

        with pytest.raises(ValidationError):
            Desuprofile.from_dict(malformed_birth_date)

        malformed_email = dict(
            id=2559,
            username="japsu",
            email="look no at sign.fi",
            first_name="Foo",
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date="2014-04-24",
        )

        with pytest.raises(ValidationError):
            Desuprofile.from_dict(malformed_email)

    def test_quirks(self):
        # Desuprofile gives null instead of missing key or empty string for birth_date
        null_birth_date = dict(
            id=2559,
            username="japsu",
            email="foo@bar.fi",
            first_name="Foo",
            last_name="Bar",
            nickname="Quux",
            phone="",
            birth_date=None,
        )

        Desuprofile.from_dict(null_birth_date)


class DesuprogrammeFeedbackTestCase(TestCase):
    def test_desuprogramme_import(self):
        programme, unused = Programme.get_or_create_dummy()
        payload = dict(
            feedback="Oli ihan kakka",
            desucon_username="japsu",
            anonymous=False,
            ip_address="127.0.0.1",
        )

        feedback = DesuprogrammeFeedback.from_dict(payload)
        feedback.save(programme)

        feedback = ProgrammeFeedback.objects.get()
        assert feedback.programme == programme
        assert feedback.author is None

    def test_hilzun_400(self):
        json = '{"feedback": "Test", "anonymous": true, "ip_address": "127.0.0.1", "desucon_username": ""}'
        programme, unused = Programme.get_or_create_dummy()

        feedback = DesuprogrammeFeedback.from_json(json)
        feedback.save(programme)
