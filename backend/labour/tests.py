from io import BytesIO

import pytest

from access.models import CBACEntry
from core.csv_export import export_csv
from core.models import Person
from event_log_v2.models.entry import Entry

from .models import JobCategory, LabourEventMeta, Qualification, Signup


@pytest.mark.django_db
def test_event_adminship():
    # TODO find out how to hook this up to pytest.mark.django_db
    Entry.ensure_partitions()

    person, _ = Person.get_or_create_dummy(superuser=False)
    labour_event_meta, _ = LabourEventMeta.get_or_create_dummy()

    assert not labour_event_meta.is_user_admin(person.user)

    labour_event_meta.admin_group.user_set.add(person.user)
    CBACEntry.ensure_admin_group_privileges_for_event(labour_event_meta.event)

    assert labour_event_meta.is_user_admin(person.user)


@pytest.mark.django_db
def test_event_adminship_superuser():
    """
    Under CBAC, superusers are no longer event managers by default (they can sudo though).
    """
    person, _ = Person.get_or_create_dummy(superuser=True)
    labour_event_meta, _ = LabourEventMeta.get_or_create_dummy()

    assert not labour_event_meta.is_user_admin(person.user)


@pytest.mark.django_db
def test_qualifications():
    person, _ = Person.get_or_create_dummy()
    qualification1, qualification2 = Qualification.get_or_create_dummies()
    jc1, jc2 = JobCategory.get_or_create_dummies()

    jc1.required_qualifications.add(qualification1)

    assert not jc1.is_person_qualified(person)
    assert jc2.is_person_qualified(person)

    person.qualifications.create(qualification=qualification2)

    assert not jc1.is_person_qualified(person)
    assert jc2.is_person_qualified(person)

    person.qualifications.create(qualification=qualification1)

    assert jc1.is_person_qualified(person)
    assert jc2.is_person_qualified(person)


@pytest.mark.django_db
def test_get_state_query_params():
    params = Signup.get_state_query_params("accepted")

    assert params["is_active"]
    assert not params["time_accepted__isnull"]
    assert params["time_finished__isnull"]


@pytest.mark.django_db
def test_group():
    jc, _ = JobCategory.get_or_create_dummy()
    assert jc.group


@pytest.mark.django_db
def test_recipient_group():
    from mailings.models import RecipientGroup

    jc, _ = JobCategory.get_or_create_dummy()

    rg = RecipientGroup.objects.get(job_category=jc)
    assert rg.verbose_name == jc.name

    jc.name = "Let's change this"
    jc.save()

    rg = RecipientGroup.objects.get(job_category=jc)
    assert rg.verbose_name == jc.name


@pytest.mark.django_db
def test_labour_excel_export():
    signup, exists = Signup.get_or_create_dummy()
    signups = Signup.objects.filter(id=signup.id)

    with BytesIO() as output_file:
        export_csv(
            signup.event,
            Signup,
            signups,
            output_file,
            m2m_mode="separate_columns",
            dialect="xlsx",
        )
