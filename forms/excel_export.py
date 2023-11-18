from typing import Any, BinaryIO, overload

from django.db import models
from django.http import HttpResponse
from django.utils.timezone import localtime

from .models.field import Field, FieldType
from .models.form import GlobalForm, EventForm
from .models.form_response import EventFormResponse, GlobalFormResponse


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


@overload
def write_responses_as_excel(
    form: EventForm,
    responses: models.QuerySet[EventFormResponse],
    output_stream: BinaryIO | HttpResponse,
):
    pass


@overload
def write_responses_as_excel(
    form: GlobalForm,
    responses: models.QuerySet[GlobalFormResponse],
    output_stream: BinaryIO | HttpResponse,
):
    pass


def write_responses_as_excel(form, responses, output_stream):
    from core.excel_export import XlsxWriter

    output = XlsxWriter(output_stream)
    fields: list[Field] = form.validated_fields

    header_row = ["created_at"]
    header_row.extend(cell for field in fields for cell in get_header_cells(field))
    output.writerow(header_row)

    for response in form.responses.all():
        response_row = [localtime(response.created_at).replace(tzinfo=None)]
        response_row.extend(cell for field in fields for cell in get_response_cells(field, response.values))
        output.writerow(response_row)

    output.close()
