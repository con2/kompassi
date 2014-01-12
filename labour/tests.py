from django.test import TestCase


from core.models import Event, Person

from .models import LabourEventMeta


class LabourEventAdminTest(TestCase):
    def test_event_adminship(self):
        person, unused = Person.get_or_create_dummy(superuser=False)
        laboureventmeta = LabourEventMeta.create_dummy()

        assert not laboureventmeta.is_user_admin(person.user)

        laboureventmeta.admin_group.user_set.add(person.user)

        assert laboureventmeta.is_user_admin(person.user)

    def test_event_adminship_superuser(self):
        person, unused = Person.get_or_create_dummy(superuser=True)
        laboureventmeta = LabourEventMeta.create_dummy()

        assert laboureventmeta.is_user_admin(person.user)
