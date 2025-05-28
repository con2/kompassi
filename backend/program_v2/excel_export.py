import logging
from collections.abc import Iterable
from itertools import groupby
from typing import BinaryIO

from django.db import models
from django.http import HttpResponse
from django.utils.timezone import localtime

from core.excel_export import XlsxWriter
from dimensions.models.dimension import Dimension
from forms.excel_export import get_header_cells, get_response_cells
from forms.models.response import Response
from forms.models.survey import Survey

logger = logging.getLogger("kompassi")


def write_program_offers_as_excel(
    dimensions: Iterable[Dimension],
    responses: models.QuerySet[Response],
    output_stream: BinaryIO | HttpResponse,
):
    output = XlsxWriter(output_stream)

    responses_by_program_form: groupby[Survey, Response] = groupby(
        responses.order_by("form__survey", "-created_at"),
        lambda r: r.form.survey,
    )

    for program_form, program_offers in responses_by_program_form:
        output.new_worksheet(program_form.slug)
        fields = program_form.combined_fields

        header_row = ["created_at", "language"]
        header_row.extend(f"dimensions.{dimension.slug}" for dimension in dimensions)
        header_row.extend(cell for field in fields for cell in get_header_cells(field))
        output.writerow(header_row)

        for program_offer in program_offers:
            values, warnings = program_offer.get_processed_form_data(fields)

            response_row = [
                localtime(program_offer.created_at).replace(tzinfo=None),
                program_offer.form.language,
            ]
            response_row.extend(
                ", ".join(program_offer.cached_dimensions.get(dimension.slug, [])) for dimension in dimensions
            )
            response_row.extend(cell for field in fields for cell in get_response_cells(field, values, warnings))
            output.writerow(response_row)

    output.close()
