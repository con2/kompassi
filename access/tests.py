# encoding: utf-8

from unittest import TestCase as NonDatabaseTestCase

from django.test import TestCase

from core.models import Person
from labour.models import LabourEventMeta

from .utils import emailify
from .email_aliases import firstname_surname
from .models import EmailAlias, GroupEmailAliasGrant, EmailAliasType


class FakePerson(object):
    first_name = 'Santtu'
    surname = 'Pajukanta'


class EmailifyTestCase(NonDatabaseTestCase):
    def test_emailify(self):
        self.assertEqual(emailify(''), '')
        self.assertEqual(emailify('Santtu Pajukanta'), 'santtu.pajukanta')
        self.assertEqual(emailify('Kalle-Jooseppi Mäki-Kangas-Ketelä'), 'kalle-jooseppi.maki-kangas-ketela')

    def test_firstname_surname(self):
        self.assertEqual(firstname_surname(FakePerson()), 'santtu.pajukanta')


class EmailAliasesTestCase(TestCase):
    def setUp(self):
        self.meta, unused = LabourEventMeta.get_or_create_dummy()
        self.group = self.meta.get_group('admins')
        self.person, unused = Person.get_or_create_dummy()


    def test_email_alias_create(self):
        email_alias, unused = EmailAlias.get_or_create_dummy()
        self.assertEqual(email_alias.email_address, 'markku.mahtinen@example.com')

    def test_ensure_aliases(self):
        alias_type, unused = EmailAliasType.get_or_create_dummy()

        self.group_grant, unused = GroupEmailAliasGrant.objects.get_or_create(group=self.group, type=alias_type)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        self.assertEqual(alias_type.email_aliases.count(), 0)

        self.person.user.groups.add(self.group)
        GroupEmailAliasGrant.ensure_aliases(person=self.person)

        self.assertEqual(alias_type.email_aliases.count(), 1)

    def test_account_name_generator_returning_none(self):
        alias_type, unused = EmailAliasType.get_or_create_dummy(metavar='nick', defaults=dict(
            account_name_code='access.email_aliases:nick',
        ))

        self.person.nick = ''
        self.person.save()

        self.assertEqual(alias_type.email_aliases.count(), 0)

        GroupEmailAliasGrant.ensure_aliases(self.person)

        self.assertEqual(alias_type.email_aliases.count(), 0)

