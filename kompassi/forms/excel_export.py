import logging
from collections.abc import Iterable, Sequence
from typing import Any, BinaryIO

from django.http import HttpResponse
from django.utils.timezone import localtime

from kompassi.core.excel_export import XlsxWriter
from kompassi.dimensions.models.dimension import Dimension

from .models.field import Field, FieldType
from .models.projection import Projection
from .models.response import Response
from .models.survey import Survey
from .utils.process_form_data import FieldWarning
from .utils.s3_presign import satanize_presigned_url

logger = logging.getLogger(__name__)


def get_header_cells(field: Field) -> list[str]:
    header_cells: list[str] = []

    match field.type:
        case FieldType.STATIC_TEXT | FieldType.DIVIDER | FieldType.SPACER:
            pass

        case FieldType.MULTI_SELECT | FieldType.DIMENSION_MULTI_SELECT:
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

        case FieldType.MULTI_SELECT | FieldType.DIMENSION_MULTI_SELECT:
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
    survey: Survey,
    dimensions: Iterable[Dimension],
    fields: Sequence[Field],
    responses: Iterable[Response],
    output_stream: BinaryIO | HttpResponse | XlsxWriter,
):
    if isinstance(output_stream, XlsxWriter):
        output = output_stream
    else:
        output = XlsxWriter(output_stream)

    header_row = ["response.revision_created_at", "response.language"]
    profile_field_selector = survey.profile_field_selector

    for profile_field_slug in profile_field_selector:
        header_row.append(f"profile.{profile_field_slug}")

    header_row.extend(f"dimensions.{dimension.slug}" for dimension in dimensions)
    header_row.extend(cell for field in fields for cell in get_header_cells(field))
    output.writerow(header_row)

    for response in responses:
        values, warnings = response.get_processed_form_data(fields)

        response_row = [
            localtime(response.revision_created_at).replace(tzinfo=None),
            response.form.language,
        ]

        if (user := response.original_created_by) and (person := user.person):  # type: ignore
            profile = profile_field_selector.select(person)
            response_row.extend(profile.get(field_slug) for field_slug in survey.profile_field_selector)
        else:
            response_row.extend("" for _ in survey.profile_field_selector)

        response_row.extend(", ".join(response.cached_dimensions.get(dimension.slug, [])) for dimension in dimensions)
        response_row.extend(cell for field in fields for cell in get_response_cells(field, values, warnings))
        output.writerow(response_row)

    if output is not output_stream:
        # If we created a new XlsxWriter instance, we need to close it.
        # If the caller passed an existing XlsxWriter instance, we assume they will handle closing it.
        output.close()


def write_projection_as_excel(
    projection: Projection,
    projected: list[dict[str, Any]],
    output_stream: BinaryIO | HttpResponse,
):
    from kompassi.core.excel_export import XlsxWriter

    output = XlsxWriter(output_stream)

    validated = projection.validated_fields

    header_row = [splat.target_field for splat in validated.splats]
    for field_name in validated.projected_dimensions:
        header_row.append(field_name)
        header_row.append(projection.get_formatted_field_name(field_name))
    output.writerow(header_row)

    for item in projected:
        item_row = [item[splat.target_field] for splat in validated.splats]
        for field_name in validated.projected_dimensions:
            item_row.append(item[field_name])
            item_row.append(item[projection.get_formatted_field_name(field_name)])
        output.writerow(item_row)

    output.close()
