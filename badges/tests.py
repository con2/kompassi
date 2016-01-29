# encoding: utf-8

import logging

from django.test import TestCase

from core.models import Person
from labour.models import LabourEventMeta, Signup, JobCategory
from programme.models import ProgrammeEventMeta, Programme, ProgrammeRole

from .models import BadgesEventMeta, Badge


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

    def test_mixed_badges(self):
        """
        Badge printing must work with a mixed case of Person and non-Person badges.
        """