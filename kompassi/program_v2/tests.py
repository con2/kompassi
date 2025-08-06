from datetime import UTC, datetime, timedelta

import pytest
from django.db import transaction

from kompassi.access.models.email_alias_domain import EmailAliasDomain
from kompassi.core.models.person import Person
from kompassi.dimensions.models.annotation import Annotation
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.forms.models.form import Form
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey
from kompassi.involvement.models.involvement import Involvement

from ..forms.utils.extract_annotations import extract_annotations_from_responses
from .filters import ProgramFilters
from .models.meta import ProgramV2EventMeta
from .models.program import Program
from .models.schedule_item import ScheduleItem


@pytest.mark.django_db
def test_program_filters():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event

    t1 = datetime.now(UTC)
    updated_after_t1 = ProgramFilters.from_query_dict({"updated_after": [t1.isoformat()]})

    p1 = Program(event=event, title="Program 1")
    p1.save()

    s1 = ScheduleItem(
        program=p1,
        start_time=datetime.now(UTC),
        duration=timedelta(hours=1),
    ).with_mandatory_fields()
    s1.save()
    s1.refresh_dependents()

    t2 = datetime.now(UTC)
    updated_after_t2 = ProgramFilters.from_query_dict({"updated_after": [t2.isoformat()]})

    assert updated_after_t1.filter_program(event.programs.all()).count() == 1
    assert updated_after_t2.filter_program(event.programs.all()).count() == 0

    assert updated_after_t1.filter_schedule_items(event.schedule_items.all()).count() == 1
    assert updated_after_t2.filter_schedule_items(event.schedule_items.all()).count() == 0


@pytest.mark.django_db
def test_program_hosts():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event

    # after creating ProgramV2EventMeta so that aliases are created
    EmailAliasDomain.get_or_create_dummy()

    offer_program = Survey(
        event=event,
        slug="offer-program",
        app=DimensionApp.PROGRAM_V2,
        purpose=SurveyPurpose.DEFAULT,
    ).with_mandatory_fields()
    offer_program.save()
    offer_program.workflow.handle_new_survey()

    offer_program_en = Form(
        event=event,
        survey=offer_program,
        language="en",
        fields=[
            dict(
                slug="title",
                title="Title",
                type="SingleLineText",
                required=True,
            ),
            dict(
                slug="description",
                title="Description",
                type="MultiLineText",
                required=True,
            ),
        ],
    )
    offer_program_en.save()
    offer_program.workflow.handle_form_update()

    accept_invitation = Survey(
        event=event,
        slug="accept-program-invitation",
        app=DimensionApp.PROGRAM_V2,
        purpose=SurveyPurpose.INVITE,
    ).with_mandatory_fields()
    accept_invitation.save()
    accept_invitation.workflow.handle_new_survey()

    accept_invitation_en = Form(
        event=event,
        survey=accept_invitation,
        language="en",
        fields=[],
    )
    accept_invitation_en.save()
    accept_invitation.workflow.handle_form_update()

    person, _ = Person.get_or_create_dummy()
    person2, _ = Person.get_or_create_dummy(another=True, superuser=False)

    # Step 1: Offer program
    with transaction.atomic():
        program_offer = Response.objects.create(
            form=offer_program_en,
            form_data={
                "title": "Test program",
                "description": "Test description",
            },
            revision_created_by=person.user,
            ip_address="127.0.0.1",
            sequence_number=offer_program.get_next_sequence_number(),
        )
        offer_program.workflow.handle_new_response_phase1(program_offer)
    offer_program.workflow.handle_new_response_phase2(program_offer)

    (program_offer_involvement,) = event.involvements.all()
    assert program_offer_involvement.person == person
    assert program_offer_involvement.program is None
    assert program_offer_involvement.response == program_offer

    # Accept program offer
    program = Program.from_program_offer(program_offer)

    (program_host_involvement,) = event.involvements.filter(program__isnull=False)
    assert program_host_involvement.person == person
    assert program_host_involvement.program == program
    assert program_host_involvement.response == program_offer

    # Step 2: Accept program invitation
    invitation = program.invite_program_host(
        person2.email,
        survey=accept_invitation,
        language="en",
        involvement_dimensions={},
    )

    with transaction.atomic():
        accept_invitation_response = Response.objects.create(
            form=accept_invitation_en,
            form_data={},
            revision_created_by=person2.user,
            ip_address="127.0.0.1",
            sequence_number=accept_invitation.get_next_sequence_number(),
        )
        accept_invitation.workflow.handle_new_response_phase1(accept_invitation_response)

        invitation.mark_used()

        Involvement.from_accepted_invitation(
            response=accept_invitation_response,
            invitation=invitation,
            cache=event.involvement_universe.preload_dimensions(),
        )

        program.refresh_cached_fields()

    assert event.involvements.count() == 3  # offer, host, host


@pytest.mark.django_db
def test_extract_annotations():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event

    with transaction.atomic():
        person, _ = Person.get_or_create_dummy()
        person2, _ = Person.get_or_create_dummy(another=True, superuser=False)

        # after creating ProgramV2EventMeta so that aliases are created
        EmailAliasDomain.get_or_create_dummy()

        offer_program = Survey(
            event=event,
            slug="offer-program",
            app=DimensionApp.PROGRAM_V2,
            purpose=SurveyPurpose.DEFAULT,
        ).with_mandatory_fields()
        offer_program.save()
        offer_program.workflow.handle_new_survey()

        offer_program_en = Form(
            event=event,
            survey=offer_program,
            language="en",
            fields=[
                dict(
                    slug="title",
                    title="Title",
                    type="SingleLineText",
                    required=True,
                ),
                dict(
                    slug="description",
                    title="Description",
                    type="MultiLineText",
                    required=True,
                ),
                dict(
                    slug="max_participants",
                    title="Max participants",
                    type="NumberField",
                    required=False,
                ),
            ],
        )
        offer_program_en.save()
        offer_program.workflow.handle_form_update()

        accept_invitation = Survey(
            event=event,
            slug="accept-program-invitation",
            app=DimensionApp.PROGRAM_V2,
            purpose=SurveyPurpose.INVITE,
        ).with_mandatory_fields()
        accept_invitation.save()
        accept_invitation.workflow.handle_new_survey()

        accept_invitation_en = Form(
            event=event,
            survey=accept_invitation,
            language="en",
            fields=[
                dict(
                    slug="max_participants",
                    title="Max participants",
                    type="NumberField",
                    required=False,
                ),
                dict(
                    slug="is_revolving_door",
                    title="Is revolving door",
                    type="SingleCheckbox",
                    required=False,
                ),
            ],
        )
        accept_invitation_en.save()
        accept_invitation.workflow.handle_form_update()

    with transaction.atomic():
        program_offer = Response.objects.create(
            form=offer_program_en,
            form_data={
                "title": "Test Program",
                "description": "Test Description",
                "max_participants": 100,
            },
            revision_created_by=person.user,
        )
        offer_program.workflow.handle_new_response_phase1(program_offer)
    with transaction.atomic():
        offer_program.workflow.handle_new_response_phase2(program_offer)

    ea, created = UniverseAnnotation.objects.update_or_create(
        universe=meta.universe,
        annotation=Annotation.objects.get(slug="konsti:maxAttendance"),
        defaults=dict(
            is_active=True,
            form_fields=[
                "this_field_does_not_exist",
                "max_participants",
                "also_this_field_does_not_exist",
            ],
        ),
    )
    assert not created

    ea2, created = UniverseAnnotation.objects.update_or_create(
        universe=meta.universe,
        annotation=Annotation.objects.get(slug="ropecon:isRevolvingDoor"),
        defaults=dict(
            is_active=True,
            form_fields=[
                "this_field_does_not_exist",
                "is_revolving_door",
                "also_this_field_does_not_exist",
            ],
        ),
    )
    assert not created

    program1 = Program.from_program_offer(program_offer)
    assert program1.annotations["konsti:maxAttendance"] == 100
    assert "ropecon:isRevolvingDoor" not in program1.annotations

    # Test that extract_annotations works with accepted program having multiple responses
    with transaction.atomic():
        program_offer2 = Response.objects.create(
            form=offer_program_en,
            form_data={
                "title": "Test Program 2",
                "description": "Test Description 2",
                # "max_participants": "",
            },
            revision_created_by=person2.user,
        )
        offer_program.workflow.handle_new_response_phase1(program_offer2)
    with transaction.atomic():
        offer_program.workflow.handle_new_response_phase2(program_offer2)

    with transaction.atomic():
        program2 = Program.from_program_offer(program_offer2)

    with transaction.atomic():
        invitation = program2.invite_program_host(
            person2.email,
            survey=accept_invitation,
            language="en",
            involvement_dimensions={},
        )

    with transaction.atomic():
        expected_annotations2 = {
            "konsti:maxAttendance": 0,
            "ropecon:isRevolvingDoor": True,
        }

        accept_invitation_response = Response.objects.create(
            form=accept_invitation_en,
            form_data={
                "max_participants": "0",
                "is_revolving_door": "on",
            },
            revision_created_by=person2.user,
            ip_address="127.0.0.1",
            sequence_number=accept_invitation.get_next_sequence_number(),
        )
        accept_invitation.workflow.handle_new_response_phase1(accept_invitation_response)

        invitation.mark_used()

        Involvement.from_accepted_invitation(
            response=accept_invitation_response,
            invitation=invitation,
            cache=event.involvement_universe.preload_dimensions(),
        )

        program2.refresh_cached_fields()

    with transaction.atomic():
        accept_invitation.workflow.handle_new_response_phase2(accept_invitation_response)

    # isolated test: our test annotation is extracted from responses as expected
    actual_annotations2 = extract_annotations_from_responses(
        responses=[program_offer2, accept_invitation_response],
        universe_annotations=[ea, ea2],
    )
    assert actual_annotations2 == expected_annotations2

    # integration test: our test annotation is extracted as part of program workflow as expected
    program2.refresh_from_db()
    assert set(program2.validated_annotations.items()).issuperset(expected_annotations2.items())
