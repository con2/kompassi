# encoding: utf-8

from django.forms import ValidationError
from django.test import TestCase

from .utils import check_password_strength


class ExternalAuthUtilsTestCase(TestCase):
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
