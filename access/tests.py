# encoding: utf-8

from unittest import TestCase as NonDatabaseTestCase

from django.test import TestCase

from .utils import emailify
from .email_aliases import firstname_surname
from .models import EmailAlias


class FakePerson(object):
    first_name = 'Santtu'
    surname = u'Pajukanta'


class EmailifyTestCase(NonDatabaseTestCase):
    def test_emailify(self):
        self.assertEqual(emailify(u''), u'')
        self.assertEqual(emailify(u'Santtu Pajukanta'), u'santtu.pajukanta')
        self.assertEqual(emailify(u'Kalle-Jooseppi Mäki-Kangas-Ketelä'), u'kalle-jooseppi.maki-kangas-ketela')

    def test_firstname_surname(self):
        self.assertEqual(firstname_surname(FakePerson()), 'santtu.pajukanta')


class EmailAliasesTestCase(TestCase):
    def test_email_alias_create(self):
      email_alias, unused = EmailAlias.get_or_create_dummy()
      self.assertEqual(email_alias.email_address, 'markku.mahtinen@example.com')