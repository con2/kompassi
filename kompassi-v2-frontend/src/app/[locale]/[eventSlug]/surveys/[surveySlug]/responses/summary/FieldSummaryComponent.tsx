import { Fragment } from "react";
import FileUploadFieldSummaryComponent from "./FileUploadFieldSummaryComponent";
import SelectFieldSummaryComponent from "./SelectFieldSummaryComponent";
import TextFieldSummaryComponent from "./TextFieldSummaryComponent";
import {
  Choice,
  Field,
  FieldSummary,
  SelectFieldSummary,
} from "@/components/forms/models";
import { Translations } from "@/translations/en";

/// For actual choice fields, return their choices.
/// For other fields that are represented as choice fields,
/// construct synthetic choices for their summary.
function getSummaryChoices(
  fieldSummary: FieldSummary,
  field: Field,
  translations: Translations,
) {
  const { type } = field;
  const t = translations.SchemaForm;
  let choices: Choice[] = [];
  let questions: Choice[] = [];

  switch (type) {
    case "SingleCheckbox":
    case "DimensionSingleCheckbox":
      choices = [
        {
          slug: "checked",
          title: t.checkbox.checked,
        },
        {
          slug: "unchecked",
          title: t.checkbox.unchecked,
        },
      ];
      break;

    case "Tristate":
      choices = [
        {
          slug: "true",
          title: t.boolean.true,
        },
        {
          slug: "false",
          title: t.boolean.false,
        },
      ];
      break;

    case "SingleSelect":
    case "DimensionSingleSelect":
    case "MultiSelect":
    case "DimensionMultiSelect":
      choices = field.choices;
      break;

    case "RadioMatrix":
      choices = field.choices;
      questions = field.questions;
      break;

    case "NumberField":
      if (fieldSummary.type === "Select") {
        choices = Object.keys(fieldSummary.summary).map((key) => ({
          slug: key,
          title: key,
        }));
      }

    case "SingleLineText":
    case "Divider":
    case "MultiLineText":
    case "Spacer":
    case "StaticText":
    case "FileUpload":
    case "DecimalField":
    case "DateField":
    case "TimeField":
    case "DateTimeField":
    case "MultiItemField":
      // no choices
      break;

    default:
      const exhaustiveCheck: never = type;
      throw new Error(
        `FieldSummaryComponent: Unknown field type ${exhaustiveCheck}`,
      );
  }

  return { choices, questions };
}

interface Props {
  translations: Translations;
  field: Field;
  fieldSummary: FieldSummary;
}

// NOTE: if you rename this to FieldSummary,
// it'll clash with models and graphql-typegen will silently fail
export default function FieldSummaryComponent({
  translations,
  field,
  fieldSummary,
}: Props) {
  const { countResponses, countMissingResponses, type } = fieldSummary;
  const { choices, questions } = getSummaryChoices(
    fieldSummary,
    field,
    translations,
  );

  switch (type) {
    // TODO handle htmlType="number"
    case "Text":
      // TODO fix padding
      return (
        <TextFieldSummaryComponent
          fieldSummary={fieldSummary}
          translations={translations}
        />
      );

    case "SingleCheckbox":
      const singleCheckboxFieldSummary: SelectFieldSummary = {
        ...fieldSummary,
        type: "Select",
        summary: {
          checked: fieldSummary.countResponses,
          unchecked: fieldSummary.countMissingResponses,
        },
      };

      return (
        <SelectFieldSummaryComponent
          translations={translations}
          choices={choices}
          fieldSummary={singleCheckboxFieldSummary}
          showMissingResponses={false}
        />
      );

    case "Select":
      return (
        <SelectFieldSummaryComponent
          translations={translations}
          choices={choices}
          fieldSummary={fieldSummary}
        />
      );

    case "Matrix":
      const countTotalResponses = countResponses + countMissingResponses;
      return questions.map((question) => {
        const questionSummary = fieldSummary.summary[question.slug];
        const countQuestionResponses = Object.values(questionSummary).reduce(
          (a, b) => a + b,
          0,
        );
        const countQuestionMissingResponses =
          countTotalResponses - countQuestionResponses;

        const matrixFieldSummary: SelectFieldSummary = {
          countResponses: countQuestionResponses,
          countMissingResponses: countQuestionMissingResponses,
          type: "Select",
          summary: fieldSummary.summary[question.slug],
        };

        return (
          <Fragment key={question.slug}>
            <div className="mb-1">{question.title}</div>
            <SelectFieldSummaryComponent
              key={question.slug}
              translations={translations}
              choices={choices}
              fieldSummary={matrixFieldSummary}
            />
          </Fragment>
        );
      });

    case "FileUpload":
      return (
        <FileUploadFieldSummaryComponent
          fieldSummary={fieldSummary}
          translations={translations}
        />
      );

    default:
      const exhaustiveCheck: never = type;
      throw new Error(
        `FieldSummaryComponent: Unknown field summary type ${exhaustiveCheck}`,
      );
  }
}
