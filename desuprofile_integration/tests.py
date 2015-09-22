# encoding: utf-8

from django.forms import ValidationError
from django.test import TestCase

from jsonschema import ValidationError

from .models import Desuprofile


class DesuprofileValidationTestCase(TestCase):
    def test_idempotence(self):
        valid_profile = dict(
            id=2559,
            email='foo@bar.fi', # required
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        self.assertEquals(Desuprofile.from_dict(valid_profile)._asdict(), valid_profile)

    def test_desuprofile_without_required_attributes(self):
        blank_email = dict(
            id=2559,
            email='', # required
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(blank_email)

        missing_first_name = dict(
            id=2559,
            email='foo@bar.fi',
            # first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(missing_first_name)

    def test_invalid_values(self):
        malformed_birth_date = dict(
            id=2559,
            email='foo@bar.fi',
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04b-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(malformed_birth_date)

        malformed_email = dict(
            id=2559,
            email='look no at sign.fi',
            first_name='Foo',
            last_name='Bar',
            nickname='Quux',
            phone='',
            birth_date='2014-04-24',
        )

        with self.assertRaises(ValidationError):
            Desuprofile.from_dict(malformed_email)

