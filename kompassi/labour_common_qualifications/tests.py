from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from kompassi.core.models import Person
from kompassi.labour.models import PersonQualification, Qualification

from .models import JVKortti


class JVKorttiTest(TestCase):
    def test_card_number(self):
        """
        Tests that only well-formed JV card numbers are accepted.
        """

        person, unused = Person.get_or_create_dummy()
        qualification = Qualification.create_dummy()
        personqualification = PersonQualification.objects.create(
            person=person,
            qualification=qualification,
        )

        today = date.today()

        valid_examples = [
            "8330/J1234/09",
            "8520/J0000/13",
        ]

        for valid_example in valid_examples:
            JVKortti(
                personqualification=personqualification, card_number=valid_example, expiration_date=today
            ).full_clean()

        invalid_examples = [
            "lol",
            # '8330/J1234/0', # need more lax validation due to new cards having a new format
            None,
            "",
        ]

        for invalid_example in invalid_examples:
            invalid = JVKortti(
                personqualification=personqualification, card_number=invalid_example, expiration_date=today
            )
            with pytest.raises(ValidationError):
                invalid.full_clean()
