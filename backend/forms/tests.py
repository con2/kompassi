import yaml

from .excel_export import get_header_cells, get_response_cells
from .models.field import Choice, Field, FieldType
from .utils.merge_form_fields import _merge_choices, _merge_fields
from .utils.process_form_data import FieldWarning, process_form_data
from .utils.summarize_responses import (
    MatrixFieldSummary,
    SelectFieldSummary,
    TextFieldSummary,
    summarize_responses,
)


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


def test_merge_choices():
    lhs_choices = [
        Choice(slug="foo", title="Foo"),
        Choice(slug="bar", title="Bar"),
        Choice(slug="quux", title="Quux"),
    ]

    rhs_choices = [
        Choice(slug="bar", title="Bar"),
        Choice(slug="baz", title="Baz"),
    ]

    expected_merged_choices = [
        Choice(slug="foo", title="Foo"),
        Choice(slug="bar", title="Bar"),
        Choice(slug="quux", title="Quux"),
        Choice(slug="baz", title="Baz"),
    ]

    assert _merge_choices(lhs_choices, rhs_choices) == expected_merged_choices


def test_merge_fields():
    lhs_fields = [
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInBoth",
        ),
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInLhs",
        ),
    ]

    rhs_fields = [
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInBoth",
        ),
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInRhs",
        ),
    ]

    expected_merged_fields = [
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInBoth",
        ),
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInLhs",
        ),
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="presentInRhs",
        ),
    ]

    assert _merge_fields(lhs_fields, rhs_fields) == expected_merged_fields


def test_summarize_responses():
    choices = [
        Choice(slug="choice1", title="Choice 1"),
        Choice(slug="choice2", title="Choice 2"),
        Choice(slug="choice3", title="Choice 3"),
    ]

    fields = [
        Field(
            type=FieldType.SINGLE_LINE_TEXT,
            slug="singleLineText",
        ),
        Field(
            type=FieldType.DIVIDER,
            slug="dividerShouldNotBePresentInSummary",
        ),
        Field(
            type=FieldType.SINGLE_SELECT,
            slug="singleSelect",
            choices=choices,
        ),
        Field(
            type=FieldType.MULTI_SELECT,
            slug="multiSelect",
            choices=choices,
        ),
        Field(
            type=FieldType.RADIO_MATRIX,
            slug="radioMatrix",
            questions=[
                Choice(
                    slug="foo",
                    title="Foo",
                ),
                Choice(
                    slug="bar",
                    title="Bar",
                ),
            ],
            choices=choices,
        ),
    ]

    responses = [
        {
            "singleLineText": "Hello world",
            "singleSelect": "choice1",
            "multiSelect": ["choice1", "choice3"],
            "radioMatrix": {
                "foo": "choice1",
                "bar": "choice2",
            },
        },
        {
            "singleLineText": "Hello world",
            "singleSelect": "choice2",
            "multiSelect": [],
            "radioMatrix": {
                "foo": "choice2",
                "bar": "choice2",
            },
        },
        # surprise choice that is not included in choices!
        # an admin may have removed it from the form after the response was submitted
        {
            "singleSelect": "choice666",
            "multiSelect": ["choice666"],
            "radioMatrix": {
                "foo": "choice666",
                # did not answer this question
                # "bar": "choice666",
            },
        },
    ]

    expected_summary = {
        "singleLineText": TextFieldSummary(
            countResponses=2,
            countMissingResponses=1,
            type=FieldType.SINGLE_LINE_TEXT,
            summary=["Hello world", "Hello world"],
        ),
        "singleSelect": SelectFieldSummary(
            countResponses=3,
            countMissingResponses=0,
            type=FieldType.SINGLE_SELECT,
            summary={"choice1": 1, "choice2": 1, "choice3": 0, "choice666": 1},
        ),
        "multiSelect": SelectFieldSummary(
            countResponses=2,
            countMissingResponses=1,
            type=FieldType.MULTI_SELECT,
            summary={"choice1": 1, "choice2": 0, "choice3": 1, "choice666": 1},
        ),
        "radioMatrix": MatrixFieldSummary(
            countResponses=3,
            countMissingResponses=0,
            type=FieldType.RADIO_MATRIX,
            summary={
                "foo": {"choice1": 1, "choice2": 1, "choice3": 0, "choice666": 1},
                "bar": {"choice1": 0, "choice2": 2, "choice3": 0},
            },
        ),
    }

    assert summarize_responses(fields, responses) == expected_summary
