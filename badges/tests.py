# encoding: utf-8

import logging
from unittest import skip

from django.test import TestCase

from core.models import Person
from labour.models import LabourEventMeta, Signup, JobCategory, PersonnelClass
from programme.models import ProgrammeEventMeta, Programme, ProgrammeRole

from .models import BadgesEventMeta, Badge, Batch


logger = logging.getLogger('kompassi')


class BadgesTestCase(TestCase):
    def setUp(self):
        self.meta, unused = BadgesEventMeta.get_or_create_dummy()
        LabourEventMeta.get_or_create_dummy()
        ProgrammeEventMeta.get_or_create_dummy()

        self.event = self.meta.event
        self.person, unused = Person.get_or_create_dummy()

    def test_condb_423(self):
        """
        Even though a worker has requested to only show their nick or first name on their badge,
        some events have decided that the real name must always be visible.

        We assume this setting is not changed midway. If it is, all badges must be revoked.
        """
        self.person.preferred_name_display_style = 'nick'
        self.person.save()

        assert self.person.first_name not in self.person.display_name
        assert self.person.surname not in self.person.display_name

        signup, unused = Signup.get_or_create_dummy(accepted=True)

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert not badge.is_first_name_visible
        assert not badge.is_surname_visible

        self.meta.real_name_must_be_visible = True
        self.meta.save()

        badge.revoke()
        signup.apply_state()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.is_first_name_visible
        assert badge.is_surname_visible

    def test_condb_424(self):
        """
        If the job title of the worker changes while the badge has not been printed yet, the change
        should be reflected in the badge.
        """

        signup, unused = Signup.get_or_create_dummy(accepted=True)

        # No explicit job title
        signup.job_title = u''
        signup.save()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created

        jc1 = signup.job_categories_accepted.first()
        assert badge.job_title == jc1.name

        jc2, unused = JobCategory.get_or_create_dummy(name=u'Hitman')
        signup.job_categories_accepted = [jc2]
        signup.save()
        signup.apply_state()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == jc2.name

        # Explicit job title should override
        title = u'Chief Hitman Commander to the Queen'
        signup.job_title = title
        signup.save()
        signup.apply_state()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == title

        # Removing explicit job title should reset to job category based title
        signup.job_title = u''
        signup.save()
        signup.apply_state()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == jc2.name

    def test_condb_429(self):
        """
        If a badge is revoked before it is printed or assigned into a batch, there is no need to
        leave it around revoked, it can be removed altogether.

        In this test, we arbitrarily revoke the badge of a worker who is still signed up to the event.
        Thus calling Badge.get_or_create again will re-create (or un-revoke) their badge.
        """
        signup, unused = Signup.get_or_create_dummy(accepted=True)
        badge, created = Badge.get_or_create(person=self.person, event=self.event)

        assert not created
        assert not badge.is_printed
        badge = badge.revoke()

        assert badge is None
        assert not Badge.objects.filter(person=self.person, personnel_class__event=self.event).exists()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert created

        batch = Batch.create(event=self.event)

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.batch == batch
        assert not badge.is_printed

        badge = badge.revoke()
        assert badge is not None
        assert badge.is_revoked

        badge = Badge.objects.get(person=self.person, personnel_class__event=self.event)

        assert not created
        assert badge.is_revoked

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert created
        assert not badge.is_revoked




    @skip("https://jira.tracon.fi/browse/CONDB-137")
    def test_condb_137(self):
        """
        If the personnel class of the worker changes, the badge shall be revoked and a new one issued.
        """

        pc2, unused = PersonnelClass.get_or_create_dummy(name='Sehr Wichtig Fellow', priority=-10)

        signup, unused = Signup.get_or_create_dummy(accepted=True)
        pc1 = signup.personnel_classes.get()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == pc1

        signup.personnel_classes.add(pc2)
        signup.apply_state()

        badge, created = Badge.get_or_create(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == pc2
