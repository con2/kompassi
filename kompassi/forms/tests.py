from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
import yaml
from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import RequestFactory
from django.utils.timezone import now

from kompassi.access.models.cbac_entry import CBACEntry
from kompassi.core.middleware import RequestLocalCache
from kompassi.core.models import Event, Person
from kompassi.core.utils.cleanup import perform_cleanup
from kompassi.dimensions.graphql.mutations.put_dimension import PutDimension
from kompassi.dimensions.models.dimension import Dimension, ValueOrdering
from kompassi.dimensions.models.dimension_value import DimensionValue
from kompassi.dimensions.models.enums import DimensionApp
from kompassi.event_log_v2.models.entry import Entry
from kompassi.graphql_api.schema import schema
from kompassi.involvement.models.enums import InvolvementType
from kompassi.involvement.models.involvement import Involvement
from kompassi.involvement.models.registry import Registry
from kompassi.program_v2.workflows.program_offer import ProgramOfferWorkflow

from .excel_export import get_header_cells, get_response_cells
from .graphql.mutations.update_form_fields import UpdateFormFields
from .graphql.mutations.update_response_dimensions import UpdateResponseDimensions
from .graphql.mutations.update_survey import UpdateSurvey
from .graphql.response_limited import LimitedResponseType
from .models.enums import SurveyPurpose
from .models.field import Choice, Field, FieldType
from .models.form import Form
from .models.response import Response
from .models.splat import Splat
from .models.survey import Survey
from .utils.merge_form_fields import _merge_fields, merge_choices
from .utils.process_form_data import FieldWarning, process_form_data
from .utils.promote_field_to_dimension import promote_field_to_dimension
from .utils.s3_presign import BUCKET_NAME, S3_ENDPOINT_URL
from .utils.summarize_responses import MatrixFieldSummary, SelectFieldSummary, TextFieldSummary, summarize_responses

# pass this as the info param to mutations that do not perform CBAC checks
MOCK_INFO = SimpleNamespace(context=SimpleNamespace(user=None))


def _mock_info(*claimses: dict[str, str]):
    """
    Like MOCK_INFO, but for mutations that perform CBAC checks via Workflow.check_access:
    grants exactly the given claims (see RequestLocalCache.mock_permissions). Workflow.check_access
    only unwraps its first argument's `.context` when it is an actual graphene ResolveInfo, so
    (unlike MOCK_INFO) this is the request itself, not an info object wrapping one.
    """
    cache = RequestLocalCache(None)  # type: ignore
    cache.mock_permissions(*claimses)
    return SimpleNamespace(user=None, kompassi_cache=cache)


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

            # tristate fields
            - type: Tristate
              slug: tristateTrue
              title: Tristate true
            - type: Tristate
              slug: tristateFalse
              title: Tristate false
            - type: Tristate
              slug: tristateUnset
              title: Tristate unset
            - type: Tristate
              slug: tristateRequiredMissing
              required: true
              title: A required tristate field that is missing

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
        # single checkbox fields
        "thisIsFalse",
        "thisIsTrue",
        "singleCheckboxRequiredMissing",
        # tristate fields
        "tristateTrue",
        "tristateFalse",
        "tristateUnset",
        "tristateRequiredMissing",
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
        # single checkbox fields
        "thisIsTrue": "on",
        # tristate fields
        "tristateTrue": "true",
        "tristateFalse": "false",
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
        # single checkbox fields
        thisIsTrue=True,
        thisIsFalse=False,
        # tristate fields
        tristateTrue=True,
        tristateFalse=False,
        tristateUnset=None,
        tristateRequiredMissing=None,
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
        # tristate fields
        tristateRequiredMissing=[FieldWarning.REQUIRED_MISSING],
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
        # thisIsFalse
        False,
        # thisIsTrue
        True,
        # singleCheckboxRequiredMissing
        False,
        # tristateTrue
        True,
        # tristateFalse
        False,
        # tristateUnset
        None,
        # tristateRequiredMissing
        None,
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

    response_row = [cell for field in fields for cell in get_response_cells(field, values, warnings)]
    assert response_row == expected_response_row


def test_process_form_data_file_upload():
    """
    Presigning S3 URLs is an offline operation, so we can test it without mocking
    """
    fields = [
        Field(slug="fileUpload", type=FieldType.FILE_UPLOAD),
        Field(slug="multiFileUpload", type=FieldType.FILE_UPLOAD, multiple=True),
        Field(slug="fileUploadRequiredMissing", type=FieldType.FILE_UPLOAD, required=True),
        Field(slug="fileUploadInvalidUrl", type=FieldType.FILE_UPLOAD),
        Field(slug="fileUploadBogusValue", type=FieldType.FILE_UPLOAD),
    ]

    # for file upload, the form data item is a list of S3 URLs
    form_data = {
        "fileUpload": [f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/file1.txt"],
        "multiFileUpload": [
            f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/file2.txt",
            f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/file3.txt",
        ],
        "fileUploadInvalidUrl": ["https://example.com/file.txt"],
        "fileUploadBogusValue": "not a list",
    }

    expected_warnings = dict(
        fileUploadRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        fileUploadInvalidUrl=[FieldWarning.INVALID_VALUE],
        fileUploadBogusValue=[FieldWarning.INVALID_VALUE],
    )

    values, warnings = process_form_data(fields, form_data)
    assert warnings == expected_warnings

    def is_valid_presigned_url(url: str):
        return url.startswith(f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/") and "?" in url

    assert all(is_valid_presigned_url(url) for url in values["fileUpload"])
    assert all(is_valid_presigned_url(url) for url in values["multiFileUpload"])
    assert "fileUploadRequiredMissing" not in values
    assert "fileUploadInvalidUrl" not in values


def test_process_form_data_number_field():
    fields = [
        Field(slug="numberField", type=FieldType.NUMBER_FIELD),
        Field(slug="numberFieldRequiredMissing", type=FieldType.NUMBER_FIELD, required=True),
        Field(slug="numberFieldInvalidValue", type=FieldType.NUMBER_FIELD),
        # XXX Not sure if this case should be supported at all. It won't be offered in UI.
        # Difference is NumberField[decimalPlaces] is represented as float and serialized as JS number
        # whereas DecimalField is represented as Decimal and serialized as string.
        Field(
            slug="numberFieldWithDecimalPlaces",
            type=FieldType.NUMBER_FIELD,
            decimal_places=2,
        ),
    ]

    form_data = {
        "numberField": "123",
        "numberFieldInvalidValue": "not a number",
        "numberFieldWithDecimalPlaces": "1.23",
    }

    expected_values = dict(
        numberField=123,
        numberFieldWithDecimalPlaces=1.23,
    )

    expected_warnings = dict(
        numberFieldRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        numberFieldInvalidValue=[FieldWarning.INVALID_VALUE],
    )

    values, warnings = process_form_data(fields, form_data)
    assert values == expected_values
    assert warnings == expected_warnings


def test_process_form_data_decimal_field():
    fields = [
        Field(slug="decimalField", type=FieldType.DECIMAL_FIELD),
        Field(slug="decimalFieldWithDecimalPlaces", type=FieldType.DECIMAL_FIELD, decimal_places=2),
        Field(slug="decimalFieldRequiredMissing", type=FieldType.DECIMAL_FIELD, required=True),
        Field(slug="decimalFieldInvalidValue", type=FieldType.DECIMAL_FIELD),
        Field(slug="decimalWithDifferingDecimalPlaces1", type=FieldType.DECIMAL_FIELD, decimal_places=2),
        Field(slug="decimalWithDifferingDecimalPlaces2", type=FieldType.DECIMAL_FIELD, decimal_places=2),
    ]

    form_data = {
        "decimalField": "123",
        "decimalFieldWithDecimalPlaces": "1.23",
        "decimalFieldInvalidValue": "not a number",
        "decimalWithDifferingDecimalPlaces1": "4",
        "decimalWithDifferingDecimalPlaces2": "3.4324",
    }

    expected_values = dict(
        decimalField="123",
        decimalFieldWithDecimalPlaces="1.23",
        decimalWithDifferingDecimalPlaces1="4.00",
        decimalWithDifferingDecimalPlaces2="3.43",
    )

    expected_warnings = dict(
        decimalFieldRequiredMissing=[FieldWarning.REQUIRED_MISSING],
        decimalFieldInvalidValue=[FieldWarning.INVALID_VALUE],
    )

    values, warnings = process_form_data(fields, form_data)
    assert values == expected_values
    assert warnings == expected_warnings


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

    assert merge_choices(lhs_choices, rhs_choices) == expected_merged_choices


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
            type=FieldType.NUMBER_FIELD,
            slug="numberField",
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
            "numberField": 5,
            "singleSelect": "choice1",
            "multiSelect": ["choice1", "choice3"],
            "radioMatrix": {
                "foo": "choice1",
                "bar": "choice2",
            },
        },
        {
            "singleLineText": "Hello world",
            "numberField": 6,
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
            count_responses=2,
            count_missing_responses=1,
            summary=["Hello world", "Hello world"],
        ),
        "numberField": SelectFieldSummary(
            count_responses=2,
            count_missing_responses=1,
            summary={"5": 1, "6": 1},
        ),
        "singleSelect": SelectFieldSummary(
            count_responses=3,
            count_missing_responses=0,
            summary={"choice1": 1, "choice2": 1, "choice3": 0, "choice666": 1},
        ),
        "multiSelect": SelectFieldSummary(
            count_responses=2,
            count_missing_responses=1,
            summary={"choice1": 1, "choice2": 0, "choice3": 1, "choice666": 1},
        ),
        "radioMatrix": MatrixFieldSummary(
            count_responses=3,
            count_missing_responses=0,
            summary={
                "foo": {"choice1": 1, "choice2": 1, "choice3": 0, "choice666": 1},
                "bar": {"choice1": 0, "choice2": 2, "choice3": 0},
            },
        ),
    }

    assert summarize_responses(fields, responses) == expected_summary


@pytest.mark.django_db
def test_lift_and_set_dimensions():
    event, _created = Event.get_or_create_dummy()

    survey = Survey.objects.create(
        event=event,
        slug="test-survey",
    )

    dimension = Dimension.objects.create(
        universe=survey.universe,
        slug="test-dimension",
    )

    DimensionValue.objects.bulk_create(
        [
            DimensionValue(
                dimension=dimension,
                slug="test-dimension-value-1",
            ),
            DimensionValue(
                dimension=dimension,
                slug="test-dimension-value-2",
            ),
        ]
    )

    dimension2 = Dimension.objects.create(
        universe=survey.universe,
        slug="test-dimension2",
        title_en="Test dimension 2",
    )

    DimensionValue.objects.bulk_create(
        [
            DimensionValue(
                dimension=dimension2,
                slug="test-dimension2-value-1",
            ),
            DimensionValue(
                dimension=dimension2,
                slug="test-dimension2-value-2",
            ),
        ]
    )

    form = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[
            dict(
                slug="test-dimension",
                type="DimensionSingleSelect",
                dimension="test-dimension",
            )
        ],
    )

    response = Response.objects.create(
        form=form,
        form_data={"test-dimension": "test-dimension-value-1"},
    )

    survey.workflow.handle_new_response_phase1(response)
    survey.workflow.handle_new_response_phase2(response)

    response.refresh_from_db()

    assert response.cached_dimensions == {
        "test-dimension": ["test-dimension-value-1"],
    }

    # also tests set_dimension_values
    # XXX: Graphene does some deep magic that causes using UpdateResponseDimensionsInput
    # as a value type to fail, so we have to use SimpleNamespace instead
    UpdateResponseDimensions.mutate(
        None,
        _mock_info(dict(app="forms")),
        SimpleNamespace(
            event_slug=event.slug,
            survey_slug=survey.slug,
            response_id=response.id,
            form_data={
                # SingleSelect used as dimension field
                "test-dimension": "test-dimension-value-2",
                # MultiSelect used as dimension field
                "test-dimension2.test-dimension2-value-1": "checked",
                "test-dimension2.test-dimension2-value-2": "checked",
            },
        ),  # type: ignore
    )

    response.refresh_from_db()

    assert set(response.cached_dimensions.keys()) == {"test-dimension", "test-dimension2"}
    assert set(response.cached_dimensions["test-dimension"]) == {"test-dimension-value-2"}
    assert set(response.cached_dimensions["test-dimension2"]) == {"test-dimension2-value-1", "test-dimension2-value-2"}


@pytest.mark.django_db
def test_put_survey_dimension():
    event, _created = Event.get_or_create_dummy()

    survey = Survey.objects.create(
        event=event,
        slug="test-survey",
    )

    # fake request and request local cache
    cache = RequestLocalCache(None)  # type: ignore
    cache.mock_permissions(dict(app="forms"))
    request = SimpleNamespace(user=None, kompassi_cache=cache)
    info = SimpleNamespace(context=request)

    # create dimension
    form_data = {
        "title_en": "Test dimension",
        "title_sv": "Testdimension",
        "isKeyDimension": "on",
        "valueOrdering": "MANUAL",
    }
    PutDimension.mutate(
        None,
        info,
        SimpleNamespace(
            scope_slug=event.scope.slug,
            universe_slug=survey.universe.slug,
            dimension_slug="test-dimension",
            form_data=form_data,
        ),  # type: ignore
    )

    dimension = Dimension.objects.get(universe=survey.universe, slug="test-dimension")

    assert dimension.slug == "test-dimension"
    assert dimension.title_en == "Test dimension"
    assert dimension.title_sv == "Testdimension"
    assert dimension.title_fi == ""
    assert dimension.is_key_dimension is True
    assert dimension.is_multi_value is False

    # update dimension
    form_data = {
        "title_en": "Test dimension",
        "title_sv": "Testdimension2",
        "isKeyDimension": "on",
        "valueOrdering": "MANUAL",
    }
    PutDimension.mutate(
        None,
        info,
        SimpleNamespace(
            scope_slug=event.scope.slug,
            universe_slug=survey.universe.slug,
            dimension_slug="test-dimension",
            form_data=form_data,
        ),  # type: ignore
    )

    dimension.refresh_from_db()
    assert dimension.title_sv == "Testdimension2"


@pytest.mark.django_db
def test_survey_without_forms():
    """
    A survey that doesn't yet have any Forms should degrade gracefully.
    """
    event, _created = Event.get_or_create_dummy()

    Survey.objects.create(
        event=event,
        slug="test-survey",
    )

    result = schema.execute(
        """
          query SurveyWithoutForms {
            event(slug: "dummy-event") {
              forms {
                survey(slug: "test-survey") {
                  title(lang: "fi")
                }
              }
            }
          }
        """,
        None,
        MOCK_INFO,
    )

    assert not result.errors


@pytest.mark.django_db
def test_refresh_cached_key_fields():
    """
    cached_key_fields is denormalized from the isKeyField flag of the form fields of the
    language version being edited, and the flag is synced to the other language versions.
    Existing responses should also have their cached_key_fields refreshed.
    """
    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="key-fields-survey")

    en = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[
            dict(slug="title", type="SingleLineText", isKeyField=True),
            dict(slug="description", type="MultiLineText"),
        ],
    )
    fi = Form.objects.create(
        event=event,
        survey=survey,
        language="fi",
        fields=[
            dict(slug="title", type="SingleLineText"),
            dict(slug="description", type="MultiLineText"),
        ],
    )

    response = Response.objects.create(
        form=en,
        form_data={
            "title": "Existing title",
            "description": "Existing description",
        },
    )

    survey.refresh_cached_key_fields(en)

    survey.refresh_from_db()
    assert survey.cached_key_fields == ["title"]

    # the isKeyField flag is synced to the other language version
    fi.refresh_from_db()
    assert next(field for field in fi.fields if field["slug"] == "title").get("isKeyField") is True
    assert all(not field.get("isKeyField") for field in fi.fields if field["slug"] != "title")

    # Existing responses get refreshed when key field selection changes.
    en.fields = [
        dict(slug="title", type="SingleLineText"),
        dict(slug="description", type="MultiLineText", isKeyField=True),
    ]
    en.save(update_fields=["fields", "cached_enriched_fields"])

    survey.refresh_cached_key_fields(en)

    survey.refresh_from_db()
    response.refresh_from_db()
    assert survey.cached_key_fields == ["description"]
    assert response.cached_key_fields == {"description": "Existing description"}


@pytest.mark.django_db
def test_update_form_fields_strips_dimension_choices():
    """
    Choices for dimension fields must only ever come from live enrichment (Form._enrich_field).
    If the editor's client-supplied choices (see injectChoices in FormEditor.tsx) were persisted
    as-is, they would go stale and out of date with the dimension whenever it or its values
    are edited or translated.
    """
    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="test-survey")

    dimension = Dimension.objects.create(universe=survey.universe, slug="test-dimension")
    DimensionValue.objects.create(dimension=dimension, slug="test-value", title_en="Test value")

    form = Form.objects.create(event=event, survey=survey, language="en", fields=[])

    UpdateFormFields.mutate(
        None,
        _mock_info(dict(app="forms")),
        SimpleNamespace(
            event_slug=event.slug,
            survey_slug=survey.slug,
            language="en",
            fields=[
                dict(
                    slug="test-dimension",
                    type="DimensionSingleSelect",
                    dimension="test-dimension",
                    # simulates the stale choices the editor bakes in for display purposes
                    choices=[dict(slug="test-value", title="Stale title")],
                ),
            ],
        ),  # type: ignore
    )

    form.refresh_from_db()

    field = next(f for f in form.fields if f["slug"] == "test-dimension")
    assert "choices" not in field

    enriched_field = next(f for f in form.cached_enriched_fields if f["slug"] == "test-dimension")
    assert enriched_field["choices"] == [dict(slug="test-value", title="Test value")]

    # Renaming the dimension value is reflected without the form ever being re-saved.
    dimension_value = dimension.values.get()
    dimension_value.title_en = "Renamed value"
    dimension_value.save()
    dimension.refresh_dependents()

    form.refresh_from_db()
    enriched_field = next(f for f in form.cached_enriched_fields if f["slug"] == "test-dimension")
    assert enriched_field["choices"] == [dict(slug="test-value", title="Renamed value")]


@pytest.mark.django_db
def test_promote_field_to_dimension():
    with transaction.atomic():
        event, _created = Event.get_or_create_dummy()

        survey = Survey.objects.create(
            event=event,
            slug="test-survey",
            app=DimensionApp.FORMS,
            purpose=SurveyPurpose.DEFAULT,
        ).with_mandatory_fields()

        form_en = Form.objects.create(
            event=event,
            survey=survey,
            language="en",
            fields=[
                dict(
                    slug="q_foo",
                    type="SingleSelect",
                    title="Foo",
                    choices=[
                        dict(
                            slug="c_bar",
                            title="Bar",
                        ),
                        dict(
                            slug="c_baz",
                            title="Baz",
                        ),
                    ],
                ),
            ],
        )

        form_fi = Form.objects.create(
            event=event,
            survey=survey,
            language="fi",
            fields=[
                dict(
                    slug="q_foo",
                    type="SingleSelect",
                    title="Foo mutta suomeksi",
                    choices=[
                        dict(
                            slug="c_bar",
                            title="Baari",
                        ),
                        # missing baz
                    ],
                ),
            ],
        )

    with transaction.atomic():
        response1 = Response.objects.create(
            form=form_en,
            form_data={
                "q_foo": "c_baz",
            },
        )
    with transaction.atomic():
        response2 = Response.objects.create(
            form=form_fi,
            form_data={
                "q_foo": "c_bar",
            },
        )
    with transaction.atomic():
        response3 = Response.objects.create(
            form=form_fi,
            form_data={},
        )

    # CASE 1: New dimension
    with transaction.atomic():
        promote_field_to_dimension(survey, "q_foo")

    dimension = survey.dimensions.get()
    assert dimension.slug == "q-foo"
    assert dimension.title_en == "Foo"
    assert dimension.title_fi == "Foo mutta suomeksi"
    assert dimension.title_sv == ""
    assert ValueOrdering(dimension.value_ordering) == ValueOrdering.MANUAL

    bar_value, baz_value = dimension.get_values("en")
    assert bar_value.slug == "c-bar"
    assert bar_value.title_en == "Bar"
    assert bar_value.title_fi == "Baari"

    assert baz_value.slug == "c-baz"
    assert baz_value.title_en == "Baz"
    assert baz_value.title_fi == ""

    response1.refresh_from_db()
    response2.refresh_from_db()
    response3.refresh_from_db()

    assert response1.cached_dimensions == {
        "q-foo": ["c-baz"],
    }
    assert response2.cached_dimensions == {
        "q-foo": ["c-bar"],
    }
    assert response3.cached_dimensions == {}

    # CASE 2: Existing dimension
    Form.objects.create(
        event=event,
        survey=survey,
        language="sv",
        fields=[
            dict(
                slug="q_foo",
                type="SingleSelect",
                title="Foo men på svenska",
                choices=[
                    # missing bar
                    dict(
                        slug="c_baz",
                        title="Baz (också på svenska)",
                    ),
                    dict(
                        slug="c_quux",
                        title="Quux (som inte finns på andra språk)",
                    ),
                ],
            ),
        ],
    )

    promote_field_to_dimension(survey, "q_foo")

    dimension = survey.dimensions.get()
    assert dimension.slug == "q-foo"
    assert dimension.title_en == "Foo"
    assert dimension.title_fi == "Foo mutta suomeksi"
    assert dimension.title_sv == "Foo men på svenska"
    assert ValueOrdering(dimension.value_ordering) == ValueOrdering.MANUAL

    bar_value, baz_value, quux_value = dimension.get_values("en")
    assert bar_value.slug == "c-bar"
    assert bar_value.title_en == "Bar"
    assert bar_value.title_fi == "Baari"
    assert bar_value.title_sv == ""

    assert baz_value.slug == "c-baz"
    assert baz_value.title_en == "Baz"
    assert baz_value.title_fi == ""
    assert baz_value.title_sv == "Baz (också på svenska)"

    assert quux_value.slug == "c-quux"
    assert quux_value.title_en == ""
    assert quux_value.title_fi == ""
    assert quux_value.title_sv == "Quux (som inte finns på andra språk)"


@pytest.mark.django_db
def test_promote_single_checkbox():
    event, _created = Event.get_or_create_dummy()

    survey = Survey.objects.create(
        event=event,
        slug="test-survey",
    )

    form_en = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[
            dict(
                slug="q_foo",
                type="SingleCheckbox",
                title="Foo",
            ),
        ],
    )

    form_fi = Form.objects.create(
        event=event,
        survey=survey,
        language="fi",
        fields=[
            dict(
                slug="q_foo",
                type="SingleCheckbox",
                title="Foo mutta suomeksi",
            ),
        ],
    )

    response1 = Response.objects.create(
        form=form_en,
        form_data={
            "q_foo": "on",
        },
    )
    response2 = Response.objects.create(
        form=form_fi,
        form_data={
            "q_foo": "",  # in case some browser represents it as q_foo=
        },
    )
    response3 = Response.objects.create(
        form=form_fi,
        form_data={},
    )

    # CASE 1: New dimension
    promote_field_to_dimension(survey, "q_foo")

    dimension = survey.dimensions.get()
    assert dimension.slug == "q-foo"
    assert dimension.title_en == "Foo"
    assert dimension.title_fi == "Foo mutta suomeksi"
    assert dimension.title_sv == ""
    assert ValueOrdering(dimension.value_ordering) == ValueOrdering.MANUAL

    true_value, false_value = dimension.get_values("en")
    assert true_value.slug == "true"
    assert true_value.title_en == "Yes"
    assert true_value.title_fi == "Kyllä"

    assert false_value.slug == "false"
    assert false_value.title_en == "No"
    assert false_value.title_fi == "Ei"

    response1.refresh_from_db()
    response2.refresh_from_db()
    response3.refresh_from_db()

    assert response1.cached_dimensions == {
        "q-foo": ["true"],
    }
    assert response2.cached_dimensions == {
        "q-foo": ["false"],
    }
    assert response3.cached_dimensions == {
        # We cannot separate unchecked and missing for checkboxes
        # because the form data is the same
        "q-foo": ["false"],
    }

    # CASE 2: Existing dimension
    Form.objects.create(
        event=event,
        survey=survey,
        language="sv",
        fields=[
            dict(
                slug="q_foo",
                type="SingleCheckbox",
                title="Foo men på svenska",
            ),
        ],
    )

    promote_field_to_dimension(survey, "q_foo")

    dimension = survey.dimensions.get()
    assert dimension.slug == "q-foo"
    assert dimension.title_en == "Foo"
    assert dimension.title_fi == "Foo mutta suomeksi"
    assert dimension.title_sv == "Foo men på svenska"
    assert ValueOrdering(dimension.value_ordering) == ValueOrdering.MANUAL

    true_value, false_value = dimension.get_values("en")
    assert true_value.slug == "true"
    assert true_value.title_en == "Yes"
    assert true_value.title_fi == "Kyllä"

    assert false_value.slug == "false"
    assert false_value.title_en == "No"
    assert false_value.title_fi == "Ei"


def test_splat():
    schema_json = [
        {
            "targetField": "name",
            "sourceFields": ["name1", "name2", "name3"],
            "required": True,
        },
        {
            "targetField": "email",
            "sourceFields": ["email1", "email2", "email3"],
            "required": False,
        },
    ]

    schema = [Splat.model_validate(item) for item in schema_json]

    values = {
        "name1": "Alice",
        "email1": "alice@example.com",
        "name2": "Bob",
        "email2": "",
        "name3": "",
        "email3": "carol@example.com",
    }

    actual = list(Splat.project(schema, values))
    expected = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": ""},
    ]
    assert actual == expected


def _perform_retention_cleanup():
    """perform_cleanup emits event log entries, which need the current month's partition."""
    Entry.ensure_partitions()
    perform_cleanup()


def _make_retention_response(
    *,
    survey_slug: str,
    retention_period: timedelta | None = None,
    default_retention_period: timedelta | None = timedelta(days=365),
    end_time: datetime | None = None,
):
    """
    A survey with one response, wired so that retention cleanup has everything it needs:
    a registry with a default retention period and an event whose end time anchors retention.

    Each call gets its own event and registry so that cases within one test, which differ
    precisely in the end time and the retention period, do not overwrite each other.
    """
    from kompassi.core.models.organization import Organization
    from kompassi.core.models.venue import Venue
    from kompassi.involvement.models.registry import Registry

    organization, _created = Organization.get_or_create_dummy()
    venue, _created = Venue.get_or_create_dummy()
    event = Event.objects.create(
        name=f"Retention test event {survey_slug}",
        slug=f"retention-{survey_slug}",
        organization=organization,
        venue=venue,
        start_time=(end_time or now()) - timedelta(days=1),
        end_time=end_time,
    )

    registry = Registry.objects.create(
        scope=organization.scope,
        slug=f"retention-{survey_slug}",
        title_en=f"Retention test registry {survey_slug}",
        default_retention_period=default_retention_period,
    )

    survey = Survey.objects.create(
        event=event,
        slug=survey_slug,
        registry=registry,
        retention_period=retention_period,
    )
    form = Form.objects.create(
        event=event,
        survey=survey,
        language="en",
        fields=[dict(slug="title", type="SingleLineText")],
    )
    response = Response.objects.create(form=form, form_data=dict(title="Personal data"))

    return survey, response


def _backdate_response(response: Response, when: datetime):
    """auto_now_add prevents setting revision_created_at on create, so backdate it afterwards."""
    Response.objects.filter(pk=response.pk).update(revision_created_at=when, original_created_at=when)


@pytest.mark.django_db
def test_response_retention_registry_default():
    """
    A response is deleted once the registry's default retention period has passed since the
    end of the year in which the event ends. A registry without a retention period retains
    indefinitely.
    """
    _survey, expired = _make_retention_response(
        survey_slug="expired-by-registry-default",
        default_retention_period=timedelta(days=365),
        end_time=now() - timedelta(days=800),
    )

    _perform_retention_cleanup()
    assert not Response.objects.filter(pk=expired.pk).exists()

    _survey, unexpired = _make_retention_response(
        survey_slug="not-yet-expired",
        default_retention_period=timedelta(days=365),
        end_time=now() - timedelta(days=300),
    )
    _survey, no_retention = _make_retention_response(
        survey_slug="retained-indefinitely",
        default_retention_period=None,
        end_time=now() - timedelta(days=4000),
    )

    _perform_retention_cleanup()
    assert Response.objects.filter(pk=unexpired.pk).exists()
    assert Response.objects.filter(pk=no_retention.pk).exists()


@pytest.mark.django_db
def test_response_retention_survey_override():
    """
    Survey.retention_period overrides the registry default in both directions: a shorter
    period expires a response the registry default would keep, and a longer one keeps a
    response the registry default would expire.
    """
    _survey, expired_by_override = _make_retention_response(
        survey_slug="shortened-by-override",
        retention_period=timedelta(days=30),
        default_retention_period=timedelta(days=4000),
        end_time=now() - timedelta(days=800),
    )
    _survey, kept_by_override = _make_retention_response(
        survey_slug="extended-by-override",
        retention_period=timedelta(days=4000),
        default_retention_period=timedelta(days=30),
        end_time=now() - timedelta(days=800),
    )

    _perform_retention_cleanup()

    assert not Response.objects.filter(pk=expired_by_override.pk).exists()
    assert Response.objects.filter(pk=kept_by_override.pk).exists()


@pytest.mark.django_db
def test_response_retention_ignores_protect_responses():
    """
    protect_responses guards against accidental deletion from the UI; the obligation to
    delete personal data once its retention period expires outranks it.
    """
    survey, response = _make_retention_response(
        survey_slug="protected-but-expired",
        end_time=now() - timedelta(days=800),
    )
    survey.protect_responses = True
    survey.save(update_fields=["protect_responses"])

    _perform_retention_cleanup()

    assert not Response.objects.filter(pk=response.pk).exists()


@pytest.mark.django_db
def test_response_retention_falls_back_to_creation_time():
    """
    An event without an end time (or an org-level scope) anchors retention on the creation
    time of the response instead.
    """
    _survey, expired = _make_retention_response(
        survey_slug="expired-by-creation-time",
        default_retention_period=timedelta(days=365),
        end_time=None,
    )
    _backdate_response(expired, now() - timedelta(days=800))

    _survey, unexpired = _make_retention_response(
        survey_slug="recent-without-end-time",
        default_retention_period=timedelta(days=365),
        end_time=None,
    )

    _perform_retention_cleanup()

    assert not Response.objects.filter(pk=expired.pk).exists()
    assert Response.objects.filter(pk=unexpired.pk).exists()


@pytest.mark.django_db
def test_response_retention_deletes_whole_revision_chain():
    """
    Expiry is decided on the current version and takes the whole revision chain with it:
    deleting only the current version would SET_NULL the old revisions' superseded_by,
    leaving them looking like current versions. Conversely an old revision whose own
    timestamps look expired is kept as long as the current version is not expired.
    """
    _survey, expired_current = _make_retention_response(
        survey_slug="expired-chain",
        default_retention_period=timedelta(days=365),
        end_time=now() - timedelta(days=800),
    )
    expired_old = Response.objects.create(
        form=expired_current.form,
        form_data=dict(title="Older personal data"),
        superseded_by=expired_current,
    )

    _survey, unexpired_current = _make_retention_response(
        survey_slug="unexpired-chain",
        default_retention_period=timedelta(days=365),
        end_time=now() - timedelta(days=100),
    )
    unexpired_old = Response.objects.create(
        form=unexpired_current.form,
        form_data=dict(title="Older personal data"),
        superseded_by=unexpired_current,
    )
    _backdate_response(unexpired_old, now() - timedelta(days=4000))

    _perform_retention_cleanup()

    assert not Response.objects.filter(pk=expired_current.pk).exists()
    assert not Response.objects.filter(pk=expired_old.pk).exists()
    assert Response.objects.filter(pk=unexpired_current.pk).exists()
    assert Response.objects.filter(pk=unexpired_old.pk).exists()


@pytest.mark.django_db
def test_response_sequence_number_survives_edits():
    """
    Editing a response assigns the new revision the next free sequence number
    (so it doesn't collide with other responses' numbers), but the GraphQL API must
    keep showing the original's number so a response's displayed ordinal never changes.
    """
    _survey, original = _make_retention_response(survey_slug="sequence-number-survives-edits")
    original.sequence_number = 1
    original.save(update_fields=["sequence_number"])

    edited = Response.objects.create(
        form=original.form,
        form_data=dict(title="Edited"),
        sequence_number=2,
    )
    original.superseded_by = edited
    original.save(update_fields=["superseded_by"])

    assert LimitedResponseType.resolve_sequence_number(edited, None) == 1
    assert LimitedResponseType.resolve_sequence_number(original, None) == 1


@pytest.mark.django_db
def test_update_survey_retention_period_days_round_trip():
    """
    UpdateSurvey exchanges retentionPeriodDays (an integer) over GraphQL but stores
    Survey.retention_period as a timedelta; both directions of that conversion, including
    clearing the override back to null, must round-trip correctly.
    """
    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(
        event=event,
        slug="test-survey",
        app=DimensionApp.FORMS,
        max_responses_per_user=1,
    )

    base_form_data = {
        "loginRequired": False,
        "maxResponsesPerUser": 1,
        "protectResponses": False,
    }

    UpdateSurvey.mutate(
        None,
        _mock_info(dict(app="forms")),
        SimpleNamespace(
            event_slug=event.slug,
            survey_slug=survey.slug,
            form_data={**base_form_data, "retentionPeriodDays": 30},
        ),  # type: ignore
    )

    survey.refresh_from_db()
    assert survey.retention_period == timedelta(days=30)

    UpdateSurvey.mutate(
        None,
        _mock_info(dict(app="forms")),
        SimpleNamespace(
            event_slug=event.slug,
            survey_slug=survey.slug,
            form_data=base_form_data,
        ),  # type: ignore
    )

    survey.refresh_from_db()
    assert survey.retention_period is None


@pytest.mark.django_db
def test_survey_clone_clones_universe_for_standalone_survey():
    """
    Cloning a stand-alone survey (app=FORMS) gives the clone its own independent copy of
    the original survey's dimensions and values, not a reference to the same Universe.
    """
    event, _created = Event.get_or_create_dummy()

    survey = Survey.objects.create(event=event, slug="clone-source")

    dimension = Dimension.objects.create(
        universe=survey.universe,
        slug="color",
        title_en="Color",
        is_key_dimension=True,
    )
    DimensionValue.objects.create(dimension=dimension, slug="red", title_en="Red")
    DimensionValue.objects.create(dimension=dimension, slug="blue", title_en="Blue")

    clone = survey.clone(
        event=event,
        slug="clone-target",
        app=DimensionApp.FORMS,
        purpose=SurveyPurpose.DEFAULT,
    )

    assert clone.universe_id != survey.universe_id
    assert clone.universe.scope_id == survey.universe.scope_id
    assert clone.universe.slug == clone.slug

    cloned_dimension = clone.universe.dimensions.get(slug="color")
    assert cloned_dimension.id != dimension.id
    assert cloned_dimension.title_en == "Color"
    assert cloned_dimension.is_key_dimension is True
    assert set(cloned_dimension.values.values_list("slug", flat=True)) == {"red", "blue"}

    # the two universes are independent: changing one does not affect the other
    DimensionValue.objects.create(dimension=cloned_dimension, slug="green", title_en="Green")
    assert set(dimension.values.values_list("slug", flat=True)) == {"red", "blue"}


@pytest.mark.django_db
def test_survey_clone_uses_target_event_program_universe():
    """
    Cloning into a program form (app=PROGRAM) uses the target event's shared program
    Universe as is; no dimensions are cloned from the source survey.
    """
    from kompassi.program_v2.models.meta import ProgramV2EventMeta

    event, _created = Event.get_or_create_dummy()
    meta, _created = ProgramV2EventMeta.get_or_create_dummy()
    target_event = meta.event

    survey = Survey.objects.create(event=event, slug="clone-source-2")
    Dimension.objects.create(universe=survey.universe, slug="color")

    dimension_count_before = target_event.program_universe.dimensions.count()

    clone = survey.clone(
        event=target_event,
        slug="clone-target-2",
        app=DimensionApp.PROGRAM,
        purpose=SurveyPurpose.DEFAULT,
    )

    assert clone.universe_id == target_event.program_universe.id
    assert clone.universe.dimensions.count() == dimension_count_before
    assert not clone.universe.dimensions.filter(slug="color").exists()


def _graphql_request(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    return request


def _cached_request(user):
    request = _graphql_request(user)
    request.kompassi_cache = RequestLocalCache(request)  # type: ignore
    return request


def _grant_org_wide(user, organization):
    return CBACEntry.objects.create(
        user=user,
        claims={"organization": organization.slug, "app": "forms"},
        valid_from=now(),
        valid_until=now() + timedelta(days=180),
    )


def _involve(person, event, registry):
    return Involvement.objects.create(
        universe=event.involvement_universe,
        person=person,
        app=DimensionApp.FORMS,
        type=InvolvementType.SURVEY_RESPONSE,
        registry=registry,
        is_active=True,
    )


SURVEY_ACCESS_CHECK_QUERY = """
  query SurveyAccessCheck($eventSlug: String!, $surveySlug: String!) {
    event(slug: $eventSlug) {
      forms {
        survey(slug: $surveySlug) {
          responses {
            id
          }
        }
      }
    }
  }
"""

INCLUDE_INACTIVE_SURVEYS_QUERY = """
  query IncludeInactiveSurveys($eventSlug: String!) {
    event(slug: $eventSlug) {
      forms {
        surveys(app: FORMS, includeInactive: true) {
          slug
        }
      }
    }
  }
"""

GRANT_SURVEY_ACCESS_MUTATION = """
  mutation GrantSurveyAccess($input: SurveyAccessInput!) {
    grantSurveyAccess(input: $input) {
      survey {
        slug
      }
    }
  }
"""

REVOKE_SURVEY_ACCESS_MUTATION = """
  mutation RevokeSurveyAccess($input: SurveyAccessInput!) {
    revokeSurveyAccess(input: $input) {
      survey {
        slug
      }
    }
  }
"""

GRANTABLE_PEOPLE_QUERY = """
  query GrantablePeople($eventSlug: String!, $surveySlug: String!, $search: String) {
    event(slug: $eventSlug) {
      forms {
        survey(slug: $surveySlug, app: FORMS) {
          canGrantAccess
          grantablePeople(search: $search) {
            id
          }
          accessGrants {
            person {
              id
            }
          }
        }
      }
    }
  }
"""


@pytest.mark.django_db
def test_per_survey_access_grant_allows_only_the_granted_survey():
    """
    Granting access to a survey grants management access to that survey only, not to
    other surveys of the same event nor to surveys of other events of the same
    organization - unlike an org-wide {organization, app} CBAC entry.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    other_event, _created = Event.get_or_create_dummy(name="Another dummy event")
    organization = event.organization

    survey_a = Survey.objects.create(event=event, slug="survey-a")
    survey_b = Survey.objects.create(event=event, slug="survey-b")
    survey_c = Survey.objects.create(event=other_event, slug="survey-c")

    registry, _created = Registry.get_or_create_dummy()

    manager, _created = Person.get_or_create_dummy(superuser=False)
    _grant_org_wide(manager.user, organization)
    manager_request = _graphql_request(manager.user)

    grantee, _created = Person.get_or_create_dummy(superuser=False, another=True)
    _involve(grantee, event, registry)
    grantee_request = _graphql_request(grantee.user)

    result = schema.execute(
        GRANT_SURVEY_ACCESS_MUTATION,
        None,
        manager_request,
        variable_values=dict(input=dict(eventSlug=event.slug, surveySlug=survey_a.slug, personId=grantee.id)),
    )
    assert not result.errors

    allowed = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        grantee_request,
        variable_values=dict(eventSlug=event.slug, surveySlug=survey_a.slug),
    )
    assert not allowed.errors

    denied_other_survey_same_event = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        grantee_request,
        variable_values=dict(eventSlug=event.slug, surveySlug=survey_b.slug),
    )
    assert denied_other_survey_same_event.errors

    denied_other_event_same_org = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        grantee_request,
        variable_values=dict(eventSlug=other_event.slug, surveySlug=survey_c.slug),
    )
    assert denied_other_event_same_org.errors


@pytest.mark.django_db
def test_org_wide_access_still_works_for_all_surveys():
    """
    Introducing survey= and universe= claims must not narrow what an org-wide
    {organization, app} CBAC entry (eg. from an admin group) already grants.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    survey_a = Survey.objects.create(event=event, slug="org-wide-survey-a")
    survey_b = Survey.objects.create(event=event, slug="org-wide-survey-b")

    admin, _created = Person.get_or_create_dummy(superuser=False)
    _grant_org_wide(admin.user, event.organization)
    admin_request = _graphql_request(admin.user)

    for survey in (survey_a, survey_b):
        result = schema.execute(
            SURVEY_ACCESS_CHECK_QUERY,
            None,
            admin_request,
            variable_values=dict(eventSlug=event.slug, surveySlug=survey.slug),
        )
        assert not result.errors

    result = schema.execute(
        INCLUDE_INACTIVE_SURVEYS_QUERY,
        None,
        admin_request,
        variable_values=dict(eventSlug=event.slug),
    )
    assert not result.errors
    assert result.data is not None
    slugs = {survey["slug"] for survey in result.data["event"]["forms"]["surveys"]}
    assert slugs == {survey_a.slug, survey_b.slug}


@pytest.mark.django_db
def test_program_survey_access_cannot_be_granted_per_survey():
    """
    Program forms (offers and invitations) are governed by event-wide program_v2 admin
    rights and cannot be granted access to on a per-survey basis.
    """
    event, _created = Event.get_or_create_dummy()
    survey = Survey(event=event, slug="program-offer-not-persisted", app=DimensionApp.PROGRAM)
    workflow = ProgramOfferWorkflow(survey=survey)

    assert workflow.access_root_claims == {}
    assert not workflow.can_access_be_granted
    assert workflow.grant_claimses == []

    manager, _created = Person.get_or_create_dummy(superuser=False)
    grantee, _created = Person.get_or_create_dummy(superuser=False, another=True)

    with pytest.raises(ValueError):
        workflow.grant_access(grantee, _graphql_request(manager.user))


@pytest.mark.django_db
def test_grant_access_refused_without_involvement_or_user():
    """
    grant_access must refuse a grant to a person who is not currently involved in the
    event, and to a person who has no user account to attach the CBACEntry to.
    """
    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="refusal-test-survey")
    registry, _created = Registry.get_or_create_dummy()

    manager, _created = Person.get_or_create_dummy(superuser=False)
    request = _graphql_request(manager.user)

    not_involved, _created = Person.get_or_create_dummy(superuser=False, another=True)
    with pytest.raises(ValueError):
        survey.workflow.grant_access(not_involved, request)

    userless = Person.objects.create(first_name="No", surname="User", email="no-user@example.com")
    _involve(userless, event, registry)
    with pytest.raises(ValueError):
        survey.workflow.grant_access(userless, request)


@pytest.mark.django_db
def test_grant_survey_access_denied_for_non_manager():
    """
    A user without any management access to the survey cannot grant others access to it.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="non-manager-test-survey")
    registry, _created = Registry.get_or_create_dummy()

    non_manager, _created = Person.get_or_create_dummy(superuser=False)
    grantee, _created = Person.get_or_create_dummy(superuser=False, another=True)
    _involve(grantee, event, registry)

    result = schema.execute(
        GRANT_SURVEY_ACCESS_MUTATION,
        None,
        _graphql_request(non_manager.user),
        variable_values=dict(input=dict(eventSlug=event.slug, surveySlug=survey.slug, personId=grantee.id)),
    )
    assert result.errors
    assert result.errors[0].extensions == {"code": "CBAC_PERMISSION_DENIED"}


@pytest.mark.django_db
def test_grantee_can_delegate_access_and_grant_can_be_revoked():
    """
    A grantee has management access and can therefore grant access onwards to another
    involved person; that second grantee sees only the survey they were granted. Revoking
    a grant removes both the survey- and universe-rooted CBACEntry and is audit logged.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    survey_a = Survey.objects.create(event=event, slug="delegation-survey-a")
    survey_b = Survey.objects.create(event=event, slug="delegation-survey-b")
    registry, _created = Registry.get_or_create_dummy()

    manager, _created = Person.get_or_create_dummy(superuser=False)
    _grant_org_wide(manager.user, event.organization)

    first_grantee, _created = Person.get_or_create_dummy(superuser=False, another=True)
    _involve(first_grantee, event, registry)

    second_grantee_user, _created = get_user_model().objects.get_or_create(username="second-grantee")
    second_grantee = Person.objects.create(
        user=second_grantee_user,
        first_name="Second",
        surname="Grantee",
        email="second@example.com",
    )
    _involve(second_grantee, event, registry)

    result = schema.execute(
        GRANT_SURVEY_ACCESS_MUTATION,
        None,
        _graphql_request(manager.user),
        variable_values=dict(input=dict(eventSlug=event.slug, surveySlug=survey_a.slug, personId=first_grantee.id)),
    )
    assert not result.errors

    # the first grantee can delegate access onwards
    result = schema.execute(
        GRANT_SURVEY_ACCESS_MUTATION,
        None,
        _graphql_request(first_grantee.user),
        variable_values=dict(input=dict(eventSlug=event.slug, surveySlug=survey_a.slug, personId=second_grantee.id)),
    )
    assert not result.errors

    second_grantee_request = _graphql_request(second_grantee.user)

    allowed = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        second_grantee_request,
        variable_values=dict(eventSlug=event.slug, surveySlug=survey_a.slug),
    )
    assert not allowed.errors

    denied = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        second_grantee_request,
        variable_values=dict(eventSlug=event.slug, surveySlug=survey_b.slug),
    )
    assert denied.errors

    assert survey_a.workflow.access_grants.count() == 2

    # revoke the first grantee's access
    result = schema.execute(
        REVOKE_SURVEY_ACCESS_MUTATION,
        None,
        _graphql_request(manager.user),
        variable_values=dict(input=dict(eventSlug=event.slug, surveySlug=survey_a.slug, personId=first_grantee.id)),
    )
    assert not result.errors

    denied_after_revoke = schema.execute(
        SURVEY_ACCESS_CHECK_QUERY,
        None,
        _graphql_request(first_grantee.user),
        variable_values=dict(eventSlug=event.slug, surveySlug=survey_a.slug),
    )
    assert denied_after_revoke.errors

    assert not CBACEntry.objects.filter(user=first_grantee.user, claims__contains={"survey": survey_a.slug}).exists()
    assert not CBACEntry.objects.filter(
        user=first_grantee.user,
        claims__contains={"universe": survey_a.universe.slug},
    ).exists()

    assert Entry.objects.filter(entry_type="access.cbacentry.created").exists()
    assert Entry.objects.filter(entry_type="access.cbacentry.deleted").exists()


@pytest.mark.django_db
def test_grantable_people_excludes_existing_grantees_and_userless_people():
    """
    grantablePeople only lists involved persons with a user account who do not already
    have per-survey access, and can be searched by name/nick/email.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    survey = Survey.objects.create(event=event, slug="grantable-people-survey")
    registry, _created = Registry.get_or_create_dummy()

    manager, _created = Person.get_or_create_dummy(superuser=False)
    _grant_org_wide(manager.user, event.organization)
    _involve(manager, event, registry)

    already_granted, _created = Person.get_or_create_dummy(superuser=False, another=True)
    _involve(already_granted, event, registry)
    survey.workflow.grant_access(already_granted, _graphql_request(manager.user))

    userless = Person.objects.create(first_name="No", surname="User", email="no-user@example.com")
    _involve(userless, event, registry)

    result = schema.execute(
        GRANTABLE_PEOPLE_QUERY,
        None,
        _graphql_request(manager.user),
        variable_values=dict(eventSlug=event.slug, surveySlug=survey.slug, search=""),
    )
    assert not result.errors
    assert result.data is not None
    survey_data = result.data["event"]["forms"]["survey"]
    assert survey_data["canGrantAccess"]

    grantable_ids = {int(person["id"]) for person in survey_data["grantablePeople"]}
    assert manager.id in grantable_ids
    assert already_granted.id not in grantable_ids
    assert userless.id not in grantable_ids

    grant_ids = {int(grant["person"]["id"]) for grant in survey_data["accessGrants"]}
    assert grant_ids == {already_granted.id}

    result = schema.execute(
        GRANTABLE_PEOPLE_QUERY,
        None,
        _graphql_request(manager.user),
        variable_values=dict(eventSlug=event.slug, surveySlug=survey.slug, search="nonexistent-search-term"),
    )
    assert not result.errors
    assert result.data is not None
    assert result.data["event"]["forms"]["survey"]["grantablePeople"] == []


@pytest.mark.django_db
def test_grantee_can_manage_dimensions_only_in_the_granted_surveys_universe():
    """
    A per-survey grant creates a second CBACEntry rooted at the survey's dimension
    Universe, so the grantee can manage that survey's dimensions but not another
    survey's dimensions, even within the same event.
    """
    Entry.ensure_partitions()

    event, _created = Event.get_or_create_dummy()
    survey_a = Survey.objects.create(event=event, slug="universe-test-survey-a")
    survey_b = Survey.objects.create(event=event, slug="universe-test-survey-b")
    registry, _created = Registry.get_or_create_dummy()

    manager, _created = Person.get_or_create_dummy(superuser=False)
    _grant_org_wide(manager.user, event.organization)

    grantee, _created = Person.get_or_create_dummy(superuser=False, another=True)
    _involve(grantee, event, registry)
    survey_a.workflow.grant_access(grantee, _graphql_request(manager.user))

    assert survey_a.universe.can_dimensions_be_created_by(_cached_request(grantee.user))
    assert not survey_b.universe.can_dimensions_be_created_by(_cached_request(grantee.user))
