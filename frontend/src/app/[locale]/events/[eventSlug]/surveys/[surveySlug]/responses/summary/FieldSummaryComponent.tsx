import SelectFieldSummaryComponent from "./SelectFieldSummaryComponent";
import TextFieldSummaryComponent from "./TextFieldSummaryComponent";
import {
  Choice,
  Field,
  FieldSummary,
  SelectFieldSummary,
} from "@/components/SchemaForm/models";
import { Translations } from "@/translations/en";

interface FieldSummaryComponentProps {
  translations: Translations;
  field: Field;
  fieldSummary: FieldSummary;
}

// NOTE: if you rename this to FieldSummary, it'll clash with models and graphql-typegen will silently fail
export default function FieldSummaryComponent({
  translations,
  field,
  fieldSummary,
}: FieldSummaryComponentProps) {
  const t = translations.Survey;

  let choices: Choice[] = [];
  let questions: Choice[] = [];

  const { countResponses, countMissingResponses } = fieldSummary;

  switch (field.type) {
    case "SingleLineText":
      if (field.htmlType === "number" && fieldSummary.type == "Select") {
        choices = Object.keys(fieldSummary.summary).map((key) => ({
          slug: key,
          title: key,
        }));
      }
      break;

    case "SingleCheckbox":
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

    case "SingleSelect":
    case "MultiSelect":
      choices = field.choices;
      break;

    case "RadioMatrix":
      choices = field.choices;
      questions = field.questions;
      break;
  }

  switch (fieldSummary.type) {
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
          <>
            <div className="mb-1">{question.title}</div>
            <SelectFieldSummaryComponent
              key={question.slug}
              translations={translations}
              choices={choices}
              fieldSummary={matrixFieldSummary}
            />
          </>
        );
      });

    default:
      return undefined;
  }
}
