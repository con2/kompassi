from django.test import TestCase


from core.models import Event, Person

from .models import LabourEventMeta


class LabourEventAdminTest(TestCase):
    def test_event_adminship(self):
        person, unused = Person.get_or_create_dummy(superuser=False)
        labour_event_meta = LabourEventMeta.create_dummy()

        assert not labour_event_meta.is_user_admin(person.user)

        labour_event_meta.admin_group.user_set.add(person.user)

        assert labour_event_meta.is_user_admin(person.user)

    def test_event_adminship_superuser(self):
        person, unused = Person.get_or_create_dummy(superuser=True)
        labour_event_meta = LabourEventMeta.create_dummy()

        assert labour_event_meta.is_user_admin(person.user)
