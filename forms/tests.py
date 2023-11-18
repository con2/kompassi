from io import BytesIO

import pytest
import yaml

from .models import Field
from .utils import process_form_data, FieldWarning
from .excel_export import write_responses_as_excel, get_header_cells, get_response_cells


def test_process_form_data():
    fields = [
        Field.model_validate(field)
        for field in yaml.safe_load(
            """
            # single line text fields
            - type: SingleLineText
              slug: singleLineText
              title: Single line text
            - type: SingleLineText
              slug: singleLineTextRequiredMissing
              title: A required field that is missing
              required: true
            - type: SingleLineText
              slug: singleLineTextHtmlNumber
              title: A number field
              htmlType: number

            # single checkbox fields
            - type: SingleCheckbox
              slug: thisIsFalse
              title: This is false
            - type: SingleCheckbox
              slug: thisIsTrue
              title: This is true
            - type: SingleCheckbox
              slug: singleCheckboxRequiredMissing
              title: A required field that is missing
              required: true

            # single select
            - type: SingleSelect
              slug: singleSelect
              title: Single select
              choices: &choices
                - slug: choice1
                  title: Choice 1
                - slug: choice2
                  title: Choice 2
                - slug: choice3
                  title: Choice 3
            - type: SingleSelect
              slug: dropdown
              title: Dropdown
              helpText: A dropdown menu shouldn't be handled any differently
              presentation: dropdown
              choices: *choices
            - type: SingleSelect
              slug: singleSelectRequiredMissing
              title: A required field that is missing
              required: true
              choices: *choices
            - type: SingleSelect
              slug: singleSelectInvalidChoice
              title: A required field with an invalid choice selected
              choices: *choices

            # multi select fields
            - type: MultiSelect
              slug: multiSelect
              title: Multi select
              choices: *choices
            - type: MultiSelect
              slug: multiSelectNothingSelected
              title: Multi select with nothing selected
              choices: *choices
            - type: MultiSelect
              slug: multiSelectRequiredMissing
              title: A required field that is missing
              required: true
              choices: *choices

            # radio matrix fields
            - type: RadioMatrix
              slug: radioMatrix
              title: Radio matrix
              questions: &questions
                - slug: foo
                  title: Foo
                - slug: bar
                  title: Bar
              choices: *choices
            - type: RadioMatrix
              slug: radioMatrixRequiredMissing
              title: A required field that has one question missing
              required: true
              questions: *questions
              choices: *choices
            - type: RadioMatrix
              slug: radioMatrixInvalidChoice
              title: A required field with an invalid choice selected
              questions: *questions
              choices: *choices
            - type: RadioMatrix
              slug: radioMatrixInvalidQuestion
              title: A required field with an invalid question
              questions: *questions
              choices: *choices
            """
        )
    ]

    header_row = [cell for field in fields for cell in get_header_cells(field)]

    expected_header_row = [
        # single line text fields
        "singleLineText",
        "singleLineTextRequiredMissing",
        "singleLineTextHtmlNumber",
        # single checkbox fields
        "thisIsFalse",
        "thisIsTrue",
        "singleCheckboxRequiredMissing",
        # single select fields
        "singleSelect",
        "dropdown",
        "singleSelectRequiredMissing",
        "singleSelectInvalidChoice",
        # multi select fields
        "multiSelect.choice1",
        "multiSelect.choice2",
        "multiSelect.choice3",
        "multiSelectNothingSelected.choice1",
        "multiSelectNothingSelected.choice2",
        "multiSelectNothingSelected.choice3",
        "multiSelectRequiredMissing.choice1",
        "multiSelectRequiredMissing.choice2",
        "multiSelectRequiredMissing.choice3",
        # radio matrix fields
        "radioMatrix.foo",
        "radioMatrix.bar",
        "radioMatrixRequiredMissing.foo",
        "radioMatrixRequiredMissing.bar",
        "radioMatrixInvalidChoice.foo",
        "radioMatrixInvalidChoice.bar",
        "radioMatrixInvalidQuestion.foo",
        "radioMatrixInvalidQuestion.bar",
    ]

    assert header_row == expected_header_row

    form_data = {
        # single line text fields
        "singleLineText": "Hello world",
        "singleLineTextHtmlNumber": "123",
        # single checkbox fields
        "thisIsTrue": "on",
        # single select fields
        "singleSelect": "choice1",
        "dropdown": "choice2",
        "singleSelectInvalidChoice": "choice666",
        # multi select fields
        "multiSelect.choice1": "on",
        "multiSelect.choice3": "on",
        # radio matrix fields
        "radioMatrix.foo": "choice1",
        "radioMatrix.bar": "choice2",
        "radioMatrixRequiredMissing.foo": "choice3",
        "radioMatrixInvalidChoice.foo": "choice666",
        "radioMatrixInvalidChoice.bar": "choice1",
        "radioMatrixInvalidQuestion.foo": "choice2",
        "radioMatrixInvalidQuestion.notFoo": "choice1",
        "radioMatrixInvalidQuestion.bar": "choice2",
    }

    expected_values = dict(
        # single line text fields
        singleLineText="Hello world",
        singleLineTextRequiredMissing="",
        singleLineTextHtmlNumber=123,
        # single checkbox fields
        thisIsTrue=True,
        thisIsFalse=False,
        # single select fields
        singleSelect="choice1",
        dropdown="choice2",
        singleSelectInvalidChoice="choice666",  # NOTE! See comment in forms/utils.py:process_form_data
        singleCheckboxRequiredMissing=False,
        singleSelectRequiredMissing="",
        # multi select fields
        multiSelect=["choice1", "choice3"],
        multiSelectNothingSelected=[],
        multiSelectRequiredMissing=[],
        # radio matrix fields
        radioMatrix={
            "foo": "choice1",
            "bar": "choice2",
        },
        radioMatrixRequiredMissing={
            "foo": "choice3",
        },
        radioMatrixInvalidChoice={
            "foo": "choice666",
            "bar": "choice1",
        },
        radioMatrixInvalidQuestion={
            "foo": "choice2",
            "notFoo": "choice1",
            "bar": "choice2",
        },
    )

    expected_warnings = dict(
        # single line text fields
        singleLineTextRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        # single checkbox fields
        singleCheckboxRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        # single select fields
        singleSelectRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        singleSelectInvalidChoice=[FieldWarning.INVALID_CHOICE],
        # multi select fields
        multiSelectRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        # radio matrix fields
        radioMatrixRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        radioMatrixInvalidChoice=[FieldWarning.INVALID_CHOICE],
        radioMatrixInvalidQuestion=[FieldWarning.INVALID_CHOICE],
    )

    values, warnings = process_form_data(fields, form_data)

    assert values == expected_values
    assert warnings == expected_warnings

    expected_response_row = [
        # singleLineText
        "Hello world",
        # singleLineTextRequiredMissing
        "",
        # singleLineTextHtmlNumber
        123,
        # thisIsFalse
        False,
        # thisIsTrue
        True,
        # singleCheckboxRequiredMissing
        False,
        # singleSelect
        "choice1",
        # dropdown
        "choice2",
        # singleSelectRequiredMissing
        "",
        # singleSelectInvalidChoice
        "choice666",
        # multiSelect.choice1
        True,
        # multiSelect.choice2
        False,
        # multiSelect.choice3
        True,
        # multiSelectNothingSelected.choice1
        False,
        # multiSelectNothingSelected.choice2
        False,
        # multiSelectNothingSelected.choice3
        False,
        # multiSelectRequiredMissing.choice1
        False,
        # multiSelectRequiredMissing.choice2
        False,
        # multiSelectRequiredMissing.choice3
        False,
        # radioMatrix.foo
        "choice1",
        # radioMatrix.bar
        "choice2",
        # radioMatrixRequiredMissing.foo
        "choice3",
        # radioMatrixRequiredMissing.bar
        "",
        # radioMatrixInvalidChoice.foo
        "choice666",
        # radioMatrixInvalidChoice.bar
        "choice1",
        # radioMatrixInvalidQuestion.foo
        "choice2",
        # radioMatrixInvalidQuestion.bar
        "choice2",
    ]

    response_row = [cell for field in fields for cell in get_response_cells(field, values)]
    assert response_row == expected_response_row

    bytesio = BytesIO()
    write_responses_as_excel(fields, [values], bytesio)

    data = bytesio.getvalue()
    assert data.startswith(b"PK")
