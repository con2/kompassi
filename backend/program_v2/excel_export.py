import logging
from collections.abc import Iterable
from itertools import groupby
from typing import BinaryIO

from django.db import models
from django.http import HttpResponse

from core.excel_export import XlsxWriter
from dimensions.models.dimension import Dimension
from forms.excel_export import write_responses_as_excel
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
