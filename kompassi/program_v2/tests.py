from datetime import UTC, datetime, timedelta

import pytest
from django.db import transaction
from django.test import RequestFactory
from django.utils.timezone import now

from kompassi.access.models.email_alias_domain import EmailAliasDomain
from kompassi.core.models.person import Person
from kompassi.dimensions.models.annotation import Annotation
from kompassi.dimensions.models.dimension import Dimension
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.dimensions.models.enums import AnnotationAppliesTo, AnnotationDataType, DimensionApp
from kompassi.dimensions.models.universe_annotation import UniverseAnnotation
from kompassi.forms.models.enums import SurveyPurpose
from kompassi.forms.models.form import Form
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey
from kompassi.involvement.models.enums import InvolvementType
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
        app=DimensionApp.PROGRAM,
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
        app=DimensionApp.PROGRAM,
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
            app=DimensionApp.PROGRAM,
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
                    propagateToAnnotation="konsti:maxAttendance",
                ),
            ],
        )
        offer_program_en.save()
        offer_program.workflow.handle_form_update()

        accept_invitation = Survey(
            event=event,
            slug="accept-program-invitation",
            app=DimensionApp.PROGRAM,
            purpose=SurveyPurpose.INVITE,
            # legacy: invites used to live in the program universe
            universe=event.program_universe,
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
                    propagateToAnnotation="konsti:maxAttendance",
                ),
                dict(
                    slug="is_revolving_door",
                    title="Is revolving door",
                    type="SingleCheckbox",
                    required=False,
                    propagateToAnnotation="ropecon:isRevolvingDoor",
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
        ),
    )
    assert not created

    ea2, created = UniverseAnnotation.objects.update_or_create(
        universe=meta.universe,
        annotation=Annotation.objects.get(slug="ropecon:isRevolvingDoor"),
        defaults=dict(
            is_active=True,
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


@pytest.mark.django_db
def test_schedule_public_from():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event

    program = Program(event=event, title="Test program")
    program.save()

    schedule_item = ScheduleItem(
        program=program,
        start_time=now(),
        duration=timedelta(hours=1),
    ).with_mandatory_fields()
    schedule_item.save()

    # public_from unset → schedule is not public
    meta.public_from = None
    meta.save(update_fields=["public_from"])
    meta.refresh_from_db()
    assert not meta.is_schedule_public

    # public_from in the future → schedule is not public
    meta.public_from = now() + timedelta(hours=1)
    meta.save(update_fields=["public_from"])
    meta.refresh_from_db()
    assert not meta.is_schedule_public

    # public_from in the past → schedule is public
    meta.public_from = now() - timedelta(seconds=1)
    meta.save(update_fields=["public_from"])
    meta.refresh_from_db()
    assert meta.is_schedule_public


@pytest.mark.django_db
def test_invite_survey_lives_in_involvement_universe_and_passes_values_forward():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event
    EmailAliasDomain.get_or_create_dummy()

    person, _ = Person.get_or_create_dummy()
    person2, _ = Person.get_or_create_dummy(another=True, superuser=False)

    offer = Survey(event=event, slug="offer", app=DimensionApp.PROGRAM, purpose=SurveyPurpose.DEFAULT)
    offer.with_mandatory_fields().save()
    offer.workflow.handle_new_survey()
    offer_en = Form(
        event=event,
        survey=offer,
        language="en",
        fields=[dict(slug="title", title="Title", type="SingleLineText", required=True)],
    )
    offer_en.save()
    offer.workflow.handle_form_update()

    invite = Survey(event=event, slug="invite", app=DimensionApp.PROGRAM, purpose=SurveyPurpose.INVITE)
    invite.with_mandatory_fields().save()
    invite.workflow.handle_new_survey()
    assert invite.universe == event.involvement_universe
    assert invite.is_in_involvement_universe
    assert offer.universe == event.program_universe

    annotation = Annotation.objects.create(
        slug="test:hostNote",
        type=AnnotationDataType.STRING,
        applies_to=AnnotationAppliesTo.INVOLVEMENT,
    )
    UniverseAnnotation.objects.create(universe=invite.universe, annotation=annotation)

    dimension = Dimension.objects.create(universe=invite.universe, slug="host-kind")
    DimensionValue.objects.create(dimension=dimension, slug="gm", title_en="GM")

    invite_en = Form(
        event=event,
        survey=invite,
        language="en",
        fields=[
            dict(slug="note", title="Note", type="SingleLineText", propagateToAnnotation="test:hostNote"),
            dict(
                slug="kind",
                title="Kind",
                type="DimensionSingleSelect",
                dimension="host-kind",
                propagateDimensionOnCreate=True,
            ),
        ],
    )
    invite_en.save()
    invite.workflow.handle_form_update()

    with transaction.atomic():
        program_offer = Response.objects.create(
            form=offer_en,
            form_data={"title": "Test program"},
            revision_created_by=person.user,
            ip_address="127.0.0.1",
            sequence_number=offer.get_next_sequence_number(),
        )
        offer.workflow.handle_new_response_phase1(program_offer)
    offer.workflow.handle_new_response_phase2(program_offer)
    program = Program.from_program_offer(program_offer)

    invitation = program.invite_program_host(
        person2.email,
        survey=invite,
        language="en",
        involvement_dimensions={},
    )

    with transaction.atomic():
        response = Response.objects.create(
            form=invite_en,
            form_data={"note": "hello", "kind": "gm"},
            revision_created_by=person2.user,
            ip_address="127.0.0.1",
            sequence_number=invite.get_next_sequence_number(),
        )
        invite.workflow.handle_new_response_phase1(response)
        invitation.mark_used()
        involvement = Involvement.from_accepted_invitation(
            response=response,
            invitation=invitation,
            cache=event.involvement_universe.preload_dimensions(),
        )
    invite.workflow.handle_new_response_phase2(response)

    assert response.cached_dimensions["host-kind"] == ["gm"]
    assert involvement.annotations["test:hostNote"] == "hello"
    assert involvement.cached_dimensions["host-kind"] == ["gm"]

    program.refresh_from_db()
    assert "test:hostNote" not in program.annotations


@pytest.mark.django_db
def test_program_followup_is_for_hosts_and_passes_values_to_their_involvements():
    meta, _ = ProgramV2EventMeta.get_or_create_dummy()
    event = meta.event
    EmailAliasDomain.get_or_create_dummy()

    host, _ = Person.get_or_create_dummy()
    outsider, _ = Person.get_or_create_dummy(another=True, superuser=False)

    offer = Survey(event=event, slug="offer", app=DimensionApp.PROGRAM, purpose=SurveyPurpose.DEFAULT)
    offer.with_mandatory_fields().save()
    offer.workflow.handle_new_survey()
    offer_en = Form(
        event=event,
        survey=offer,
        language="en",
        fields=[dict(slug="title", title="Title", type="SingleLineText", required=True)],
    )
    offer_en.save()
    offer.workflow.handle_form_update()

    followup = Survey(event=event, slug="followup", app=DimensionApp.PROGRAM, purpose=SurveyPurpose.FOLLOWUP)
    followup.with_mandatory_fields().save()
    followup.workflow.handle_new_survey()
    assert followup.universe == event.involvement_universe
    assert followup.involvement_type == InvolvementType.PROGRAM_HOST

    annotation = Annotation.objects.create(
        slug="test:diet",
        type=AnnotationDataType.STRING,
        applies_to=AnnotationAppliesTo.INVOLVEMENT,
    )
    UniverseAnnotation.objects.create(universe=followup.universe, annotation=annotation)
    followup_en = Form(
        event=event,
        survey=followup,
        language="en",
        fields=[
            dict(slug="diet", title="Diet", type="SingleLineText", propagateToAnnotation="test:diet"),
            dict(slug="note", title="Note", type="SingleLineText", propagateToAnnotation="test:diet"),
        ],
    )
    followup_en.save()
    followup.workflow.handle_form_update()

    with transaction.atomic():
        program_offer = Response.objects.create(
            form=offer_en,
            form_data={"title": "Test program"},
            revision_created_by=host.user,
            ip_address="127.0.0.1",
            sequence_number=offer.get_next_sequence_number(),
        )
        offer.workflow.handle_new_response_phase1(program_offer)
    offer.workflow.handle_new_response_phase2(program_offer)
    Program.from_program_offer(program_offer)

    def request_by(person):
        request = RequestFactory().get("/")
        request.user = person.user
        return request

    assert followup.workflow.can_be_responded_by(request_by(host))
    assert not followup.workflow.can_be_responded_by(request_by(outsider))

    with transaction.atomic():
        response = Response.objects.create(
            form=followup_en,
            form_data={"diet": "vegan"},
            revision_created_by=host.user,
            original_created_by=host.user,
            ip_address="127.0.0.1",
            sequence_number=followup.get_next_sequence_number(),
        )
        followup.workflow.handle_new_response_phase1(response)
    followup.workflow.handle_new_response_phase2(response)

    (host_involvement,) = event.involvements.filter(person=host, type=InvolvementType.PROGRAM_HOST)
    assert host_involvement.annotations["test:diet"] == "vegan"
    assert not event.involvements.filter(person=outsider).exists()

    # an edit does not pass the annotation forward unless the field says so
    with transaction.atomic():
        edited = Response.objects.create(
            form=followup_en,
            form_data={"diet": "omnivore"},
            revision_created_by=host.user,
            original_created_by=host.user,
            ip_address="127.0.0.1",
            sequence_number=followup.get_next_sequence_number(),
        )
        followup.workflow.handle_new_response_phase1(edited, old_version=response)
    host_involvement.refresh_from_db()
    assert host_involvement.annotations["test:diet"] == "vegan"
