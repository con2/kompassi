import logging
from collections.abc import Iterable
from itertools import groupby
from typing import BinaryIO

from django.db import models
from django.http import HttpResponse
from paikkala.models.tickets import Ticket as PaikkalaTicket

from kompassi.core.excel_export import XlsxWriter
from kompassi.core.models.event import Event
from kompassi.core.utils.locale_utils import get_message_in_language
from kompassi.dimensions.models.dimension import Dimension
from kompassi.forms.excel_export import write_responses_as_excel
from kompassi.forms.models.response import Response
from kompassi.forms.models.survey import Survey
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.involvement.models.profile_field_selector import ProfileFieldSelector

from .graphql.program_host_full import ProgramHost
from .models.schedule_item import ScheduleItem

logger = logging.getLogger(__name__)


def write_program_offers_as_excel(
    dimensions: Iterable[Dimension],
    responses: models.QuerySet[Response],
    output_stream: BinaryIO | HttpResponse,
):
    output = XlsxWriter(output_stream)

    responses_by_program_form: groupby[Survey, Response] = groupby(
        responses.order_by("form__survey", "-revision_created_at"),
        lambda r: r.form.survey,
    )

    for program_form, program_offers in responses_by_program_form:
        output.new_worksheet(program_form.slug)
        write_responses_as_excel(
            program_form,
            dimensions,
            program_form.combined_fields,
            list(program_offers),
            output,
        )

    output.close()


def write_program_hosts_as_excel(
    hosts: Iterable[ProgramHost],
    output_stream: BinaryIO | HttpResponse,
):
    output = XlsxWriter(output_stream)

    field_slugs = list(ProfileFieldSelector.all_fields())
    field_slugs.remove("id")
    # move last_name to front
    field_slugs.remove("last_name")
    field_slugs.insert(0, "last_name")

    output.writerow(
        [
            *field_slugs,
            "program_items",
        ]
    )

    for host in hosts:
        profile_field_selector = ProfileFieldSelector.union(
            *[involvement.profile_field_selector for involvement in host.involvements]
        )
        profile_fields = profile_field_selector.select(host.person)

        output.writerow(
            [
                *[profile_fields.get(field_slug, "") for field_slug in field_slugs],
                "\n".join(involvement.title for involvement in host.involvements if involvement.program),
            ]
        )

    output.close()


def write_schedule_items_as_excel(
    event: Event,
    schedule_items: Iterable[ScheduleItem],
    output_stream: BinaryIO | HttpResponse,
    dimensions: models.QuerySet[Dimension],
    lang: str = DEFAULT_LANGUAGE,
):
    output = XlsxWriter(output_stream)

    header_row = [
        "start_time",
        "end_time",
        "length_minutes",
        "location",
        "title",
    ]

    header_row.extend(kd.slug for kd in dimensions)
    output.writerow(header_row)

    timezone = event.timezone

    for item in schedule_items:
        row = [
            item.start_time.astimezone(timezone).replace(tzinfo=None),
            item.cached_end_time.astimezone(timezone).replace(tzinfo=None),
            item.duration.total_seconds() // 60,
            get_message_in_language(item.cached_location, lang),
            item.title,
        ]

        for dimension in dimensions:
            row.append(", ".join(item.cached_combined_dimensions.get(dimension.slug, [])))

        output.writerow(row)

    output.close()


def write_reservations_as_excel(
    tickets: models.QuerySet[PaikkalaTicket],
    output_stream: BinaryIO | HttpResponse,
):
    output = XlsxWriter(output_stream)

    header_row = [
        "zone",
        "row",
        "number",
        "surname",
        "first_name",
        "nick",
        "normalized_phone_number",
        "email",
    ]

    output.writerow(header_row)

    for ticket in tickets:
        row = [
            ticket.zone.name,
            ticket.row.name,
            ticket.number,
            ticket.user.person.surname,
            ticket.user.person.first_name,
            ticket.user.person.nick,
            ticket.user.person.normalized_phone_number,
            ticket.user.person.email,
        ]
        output.writerow(row)

    output.close()
