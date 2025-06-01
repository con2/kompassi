from datetime import UTC, datetime, timedelta

import pytest
from django.db import transaction

from access.models.email_alias_domain import EmailAliasDomain
from core.models.event import Event
from core.models.person import Person
from forms.models.enums import SurveyApp, SurveyPurpose
from forms.models.form import Form
from forms.models.response import Response
from forms.models.survey import Survey
from involvement.models.involvement import Involvement

from .filters import ProgramFilters
from .models.meta import ProgramV2EventMeta
from .models.program import Program
from .models.schedule import ScheduleItem


@pytest.mark.django_db
def test_program_filters():
    event, _ = Event.get_or_create_dummy()

    t1 = datetime.now(UTC)
    updated_after_t1 = ProgramFilters.from_query_dict({"updated_after": [t1.isoformat()]})

    p1 = Program(event=event, title="Program 1")
    p1.save()

    s1 = ScheduleItem(program=p1, start_time=datetime.now(UTC), length=timedelta(hours=1)).with_generated_fields()
    s1.save()

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
    ).with_mandatory_attributes_for_app(SurveyApp.PROGRAM_V2, SurveyPurpose.DEFAULT)
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
    ).with_mandatory_attributes_for_app(SurveyApp.PROGRAM_V2, SurveyPurpose.INVITE)
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
