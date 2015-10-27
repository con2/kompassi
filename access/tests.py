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

    def test_ensure_aliases(self):
        meta, unused = LabourEventMeta.get_or_create_dummy()
        group = meta.get_group('admins')
        alias_type, unused = EmailAliasType.get_or_create_dummy()
        person, unused = Person.get_or_create_dummy()

        group_grant, unused = GroupEmailAliasGrant.objects.get_or_create(group=group, type=alias_type)
        GroupEmailAliasGrant.ensure_aliases(person=person)

        self.assertEqual(alias_type.email_aliases.count(), 0)

        person.user.groups.add(group)
        GroupEmailAliasGrant.ensure_aliases(person=person)

        self.assertEqual(alias_type.email_aliases.count(), 1)
