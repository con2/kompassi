from typing import Any, BinaryIO, Iterable

from django.http import HttpResponse

from .models.field import Field, FieldType


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


def get_response_cells(field: Field, values: dict[str, Any]) -> list[Any]:
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

        case _:
            cells.append(values.get(field.slug, ""))

    return cells


def write_responses_as_excel(
    fields: list[Field],
    responses: Iterable[dict[str, Any]],
    output_stream: BinaryIO | HttpResponse,
):
    from core.excel_export import XlsxWriter

    output = XlsxWriter(output_stream)

    header_row = [cell for field in fields for cell in get_header_cells(field)]
    output.writerow(header_row)

    for values in responses:
        response_row = [cell for field in fields for cell in get_response_cells(field, values)]
        output.writerow(response_row)

    output.close()
