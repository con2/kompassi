from io import BytesIO

from django.test import TestCase

from access.models import CBACEntry
from core.csv_export import export_csv
from core.models import Person

from .models import JobCategory, LabourEventMeta, Qualification, Signup


class LabourEventAdminTest(TestCase):
    def test_event_adminship(self):
        person, unused = Person.get_or_create_dummy(superuser=False)
        labour_event_meta, unused = LabourEventMeta.get_or_create_dummy()

        assert not labour_event_meta.is_user_admin(person.user)

        labour_event_meta.admin_group.user_set.add(person.user)
        CBACEntry.ensure_admin_group_privileges_for_event(labour_event_meta.event)

        assert labour_event_meta.is_user_admin(person.user)

    def test_event_adminship_superuser(self):
        """
        Under CBAC, superusers are no longer event managers by default (they can sudo though).
        """
        person, unused = Person.get_or_create_dummy(superuser=True)
        labour_event_meta, unused = LabourEventMeta.get_or_create_dummy()

        assert not labour_event_meta.is_user_admin(person.user)


class QualificationTest(TestCase):
    def test_qualifications(self):
        person, unused = Person.get_or_create_dummy()
        qualification1, qualification2 = Qualification.get_or_create_dummies()
        jc1, jc2 = JobCategory.get_or_create_dummies()

        jc1.required_qualifications.add(qualification1)

        assert not jc1.is_person_qualified(person)
        assert jc2.is_person_qualified(person)

        person.personqualification_set.create(qualification=qualification2)

        assert not jc1.is_person_qualified(person)
        assert jc2.is_person_qualified(person)

        person.personqualification_set.create(qualification=qualification1)

        assert jc1.is_person_qualified(person)
        assert jc2.is_person_qualified(person)


class SignupTest(TestCase):
    def test_get_state_query_params(self):
        params = Signup.get_state_query_params("accepted")

        self.assertTrue(params["is_active"])
        self.assertFalse(params["time_accepted__isnull"])
        self.assertTrue(params["time_finished__isnull"])


class JobCategoryTestCase(TestCase):
    def test_group(self):
        jc, unused = JobCategory.get_or_create_dummy()
        assert jc.group

    def test_recipient_group(self):
        from mailings.models import RecipientGroup

        jc, unused = JobCategory.get_or_create_dummy()

        rg = RecipientGroup.objects.get(job_category=jc)
        assert rg.verbose_name == jc.name

        jc.name = "Let's change this"
        jc.save()

        rg = RecipientGroup.objects.get(job_category=jc)
        assert rg.verbose_name == jc.name


class ExcelExportTestCase(TestCase):
    def test_labour_excel_export(self):
        signup, exists = Signup.get_or_create_dummy()
        signups = Signup.objects.filter(id=signup.id)

        with BytesIO() as output_file:
            export_csv(signup.event, Signup, signups, output_file, m2m_mode="separate_columns", dialect="xlsx")
