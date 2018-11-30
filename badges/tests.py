# encoding: utf-8

import logging
from unittest import skip

from django.test import TestCase

from core.models import Person
from labour.models import LabourEventMeta, Signup, JobCategory, PersonnelClass
from programme.models import ProgrammeEventMeta, Programme, ProgrammeRole, Role

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

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert not badge.is_first_name_visible
        assert not badge.is_surname_visible

        self.meta.real_name_must_be_visible = True
        self.meta.save()

        badge.revoke()

        signup = Signup.objects.get(id=signup.id)
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
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
        signup.job_title = ''
        signup.save()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created

        jc1 = signup.job_categories_accepted.first()
        assert badge.job_title == jc1.name

        jc2, unused = JobCategory.get_or_create_dummy(name='Hitman')
        signup.job_categories_accepted.set([jc2])
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == jc2.name

        # Explicit job title should override
        title = 'Chief Hitman Commander to the Queen'
        signup.job_title = title
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == title

        # Removing explicit job title should reset to job category based title
        signup.job_title = ''
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == jc2.name

    def test_condb_429(self):
        """
        If a badge is revoked before it is printed or assigned into a batch, there is no need to
        leave it around revoked, it can be removed altogether.

        In this test, we arbitrarily revoke the badge of a worker who is still signed up to the event.
        Thus calling Badge.ensure again will re-create (or un-revoke) their badge.
        """
        signup, unused = Signup.get_or_create_dummy(accepted=True)
        badge, created = Badge.ensure(person=self.person, event=self.event)

        assert not created
        assert not badge.is_printed
        badge = badge.revoke()

        assert badge is None
        assert not Badge.objects.filter(person=self.person, personnel_class__event=self.event).exists()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert created

        batch = Batch.create(event=self.event)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.batch == batch
        assert not badge.is_printed

        badge = badge.revoke()
        assert badge is not None
        assert badge.is_revoked

        badge = Badge.objects.get(person=self.person, personnel_class__event=self.event)

        assert not created
        assert badge.is_revoked

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert created
        assert not badge.is_revoked

    def test_condb_137_intra_labour(self):
        """
        If the personnel class of the worker changes, the badge shall be revoked and a new one issued.
        """

        signup, unused = Signup.get_or_create_dummy(accepted=True)
        pc1 = signup.personnel_classes.get()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == pc1

        # Create another personnel class that is guaranteed to be higher in priority than the current one.
        pc2, unused = PersonnelClass.get_or_create_dummy(
            name='Sehr Wichtig Fellow',
            priority=pc1.priority - 10
        )

        self.event.labour_event_meta.create_groups()

        signup.personnel_classes.add(pc2)
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == pc2

    def test_condb_137_programme_to_labour(self):
        """
        Most conventions assign a higher priority (lower priority number) to volunteer workers than
        speakers and other programme hosts. This is to say, if the same person is both volunteering and
        speaking, they are supposed to get a worker badge, not a speaker badge. This is, of course,
        configurable on a per-event basis, but this is how it is in our test data.

        We model a case in which the same person is first accepted as a speaker and thus gets a speaker
        badge, and is then accepted as a volunteer worker, "promoting" them to worker status and earning
        them a worker badge.
        """
        programme_role, unused = ProgrammeRole.get_or_create_dummy()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == programme_role.role.personnel_class

        signup, created = Signup.get_or_create_dummy(accepted=True)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == signup.personnel_classes.get()

        # Now cancel the worker signup and make sure they go back to having a programme badge
        signup.personnel_classes.set([])
        signup.job_categories_accepted = []
        signup.state = 'cancelled'
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == programme_role.role.personnel_class

    def test_condb_428_labour(self):
        """
        If someone is first accepted as a worker, but then cancels their participation or they are fired,
        their badge should get revoked.
        """
        signup, created = Signup.get_or_create_dummy(accepted=True)

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == signup.personnel_classes.get()

        # Now cancel the worker signup and make sure they go back to having a programme badge
        signup.personnel_classes.set([])
        signup.job_categories_accepted = []
        signup.state = 'cancelled'
        signup.save()
        signup.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge is None

    def test_condb_428_programme(self):
        """
        If someone is first accepted as a speaker, but then cancels their programme or they are fired,
        their badge should get revoked.
        """
        programme_role, unused = ProgrammeRole.get_or_create_dummy()
        programme = programme_role.programme

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.personnel_class == programme_role.role.personnel_class

        programme.state = 'rejected'
        programme.save()
        programme.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge is None

    def test_condb_261(self):
        """
        If someone changes their name while they have outstanding badges, those badges should get revoked
        and re-created.
        """
        programme_role, unused = ProgrammeRole.get_or_create_dummy()
        programme = programme_role.programme

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.first_name == self.person.first_name

        self.person.first_name = 'Matilda'
        self.person.save()
        self.person.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.first_name == self.person.first_name


    def test_programme_roles(self):
        """
        If someone has multiple programmes, they should get the job title of the highest-priority (lowest
        priority number) Role.
        """
        programme_role, unused = ProgrammeRole.get_or_create_dummy()
        role = programme_role.role
        personnel_class = role.personnel_class
        programme = programme_role.programme

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == role.title

        programme2, unused = Programme.get_or_create_dummy(title='Cosplay-deitti')
        role2, unused = Role.get_or_create_dummy(
            personnel_class=personnel_class,
            priority=role.priority - 10,
            title='More Importanter Programme Person',
        )
        programme_Role2, unused = ProgrammeRole.get_or_create_dummy(programme=programme2, role=role2)

        programme2.apply_state()

        badge, created = Badge.ensure(person=self.person, event=self.event)
        assert not created
        assert badge.job_title == role2.title
