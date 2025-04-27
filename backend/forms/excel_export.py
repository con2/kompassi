import logging
from collections.abc import Iterable, Sequence
from typing import Any, BinaryIO

from django.db import models
from django.http import HttpResponse
from django.utils.timezone import localtime

from dimensions.models.dimension import Dimension

from .models.field import Field, FieldType
from .models.response import Response
from .utils.process_form_data import FieldWarning
from .utils.s3_presign import satanize_presigned_url

logger = logging.getLogger("kompassi")


def get_header_cells(field: Field) -> list[str]:
    header_cells: list[str] = []

    match field.type:
        case FieldType.STATIC_TEXT | FieldType.DIVIDER | FieldType.SPACER:
            pass

        case FieldType.MULTI_SELECT:
            choices = field.choices or []
            header_cells.extend(f"{field.slug}.{choice.slug}" for choice in choices)

        case FieldType.RADIO_MATRIX:
            questions = field.questions or []
            header_cells.extend(f"{field.slug}.{question.slug}" for question in questions)

        case _:
            header_cells.append(field.slug)

    return header_cells


def get_response_cells(
    field: Field,
    values: dict[str, Any],
    warnings: dict[str, list[FieldWarning]],
) -> list[Any]:
    cells = []

    match field.type:
        case FieldType.STATIC_TEXT | FieldType.DIVIDER | FieldType.SPACER:
            pass

        case FieldType.MULTI_SELECT:
            choices = field.choices or []
            cells.extend(choice.slug in values.get(field.slug, []) for choice in choices)

        case FieldType.RADIO_MATRIX:
            questions = field.questions or []
            cells.extend(values.get(field.slug, {}).get(question.slug, "") for question in questions)

        case _ if field.type.are_attachments_allowed:
            if field_warnings := warnings.get(field.slug, []):
                logger.warning(
                    "get_response_cells refusing to operate on a FileUpload field %s with warnings: %s",
                    field.slug,
                    field_warnings,
                )
                cells.append("")
            else:
                presigned_urls: list[str] = values.get(field.slug, [])
                cells.append("\n".join(satanize_presigned_url(presigned_url) for presigned_url in presigned_urls))

        case _:
            cells.append(values.get(field.slug, ""))

    return cells


def write_responses_as_excel(
    dimensions: Iterable[Dimension],
    fields: Sequence[Field],
    responses: models.QuerySet[Response],
    output_stream: BinaryIO | HttpResponse,
):
    from core.excel_export import XlsxWriter

    output = XlsxWriter(output_stream)

    header_row = ["created_at", "language"]
    header_row.extend(f"dimensions.{dimension.slug}" for dimension in dimensions)
    header_row.extend(cell for field in fields for cell in get_header_cells(field))
    output.writerow(header_row)

    for response in responses:
        values, warnings = response.get_processed_form_data(fields)

        response_row = [
            localtime(response.created_at).replace(tzinfo=None),
            response.form.language,
        ]
        response_row.extend(", ".join(response.cached_dimensions.get(dimension.slug, [])) for dimension in dimensions)
        response_row.extend(cell for field in fields for cell in get_response_cells(field, values, warnings))
        output.writerow(response_row)

    output.close()
