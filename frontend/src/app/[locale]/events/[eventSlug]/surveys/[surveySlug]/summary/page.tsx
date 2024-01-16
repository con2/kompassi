import Link from "next/link";
import { notFound } from "next/navigation";
import { ReturnLink } from "./ReturnLink";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import Linebreaks from "@/components/helpers/Linebreaks";
import {
  Field,
  Layout,
  validateFields,
  validateSummary,
  FieldSummary,
  Choice,
  SingleSelect,
  MultiSelect,
  SelectFieldSummary,
  TextFieldSummary,
  SingleCheckboxSummary,
} from "@/components/SchemaForm/models";
import SchemaFormField from "@/components/SchemaForm/SchemaFormField";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Translations } from "@/translations/en";

const query = gql(`
  query SurveySummary($eventSlug: String!, $surveySlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          fields(lang: $locale)
          summary
          countResponses
        }
      }
    }
  }
`);

interface TextFieldSummaryComponentProps {
  fieldSummary: TextFieldSummary;
  translations: Translations;
}

function TextFieldSummaryComponent({
  fieldSummary,
  translations,
}: TextFieldSummaryComponentProps) {
  const t = translations.SurveyResponse;
  const { summary, countResponses, countMissingResponses } = fieldSummary;
  return (
    <>
      {fieldSummary.summary.map((item, idx) => (
        <div key={idx} className="card mb-2">
          <div className="card-body p-2 ps-3 pe-3">
            <Linebreaks text={item} />
          </div>
        </div>
      ))}
      <p className="text-muted">
        {t.attributes.countResponses}: {countResponses}.{" "}
        {t.attributes.countMissingResponses}: {countMissingResponses}.
      </p>
    </>
  );
}

interface SelectFieldSummaryComponentProps {
  translations: Translations;
  choices: Choice[];
  fieldSummary: SelectFieldSummary;
  showMissingResponses?: boolean;
}

function SelectFieldSummaryComponent({
  translations,
  choices,
  fieldSummary,
  showMissingResponses,
}: SelectFieldSummaryComponentProps) {
  const { countResponses, countMissingResponses, summary } = fieldSummary;
  showMissingResponses ??= true;
  const t = translations.SurveyResponse;

  return (
    <table className="table table-striped table-bordered">
      <thead>
        <tr>
          <th scope="col">{t.attributes.choice}</th>
          <th scope="col">{t.attributes.percentageOfResponses}</th>
          <th scope="col">{t.attributes.countResponses}</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(summary).map(([choiceSlug, countThisChoice], idx) => {
          const choice = choices.find((c) => c.slug === choiceSlug);
          const choiceTitle = choice?.title || (
            <>
              <span title={t.warnings.choiceNotFound}>⚠️</span>{" "}
              <em>{choiceSlug}</em>
            </>
          );
          const percentage = countResponses
            ? Math.round((countThisChoice / countResponses) * 100)
            : 0;

          return (
            <tr key={choiceSlug}>
              <td className="align-middle" scope="row">
                {choiceTitle}
              </td>
              <td className="align-middle" style={{ width: "30%" }}>
                <div className="progress">
                  <div
                    className="progress-bar"
                    role="progressbar"
                    style={{
                      width: `${percentage}%`,
                    }}
                    aria-valuenow={percentage}
                    aria-valuemin={0}
                    aria-valuemax={100}
                  >
                    {percentage}%
                  </div>
                </div>
              </td>
              <td className="align-middle" style={{ width: "10%" }}>
                {countThisChoice}
              </td>
            </tr>
          );
        })}
        <tr>
          <td>
            ❓{" "}
            <em className="text-muted">{t.attributes.countMissingResponses}</em>
          </td>
          <td></td>
          <td>
            <span className="text-muted">{countMissingResponses}</span>
          </td>
        </tr>
      </tbody>
    </table>
  );
}

interface FieldSummaryComponentProps {
  translations: Translations;
  field: Field;
  fieldSummary: FieldSummary;
}

// NOTE: if you rename this to FieldSummary, it'll clash with models and graphql-typegen will silently fail
function FieldSummaryComponent({
  translations,
  field,
  fieldSummary,
}: FieldSummaryComponentProps) {
  const t = translations.SurveyResponse;

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

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.SurveyResponse;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.summaryTitle,
  });

  return { title };
}

export default async function SummaryPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.SurveyResponse;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey?.summary) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const fields = survey.fields || [];
  const summary = survey.summary;

  validateFields(fields);
  validateSummary(summary);

  return (
    <ViewContainer>
      <ReturnLink messages={t.actions} />
      <ViewHeading>
        {t.summaryTitle}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>
      {fields.map((field) => (
        <SchemaFormField
          key={field.slug}
          field={field}
          layout={Layout.Vertical}
        >
          {summary[field.slug] && (
            <FieldSummaryComponent
              translations={translations}
              field={field}
              fieldSummary={summary[field.slug]}
            />
          )}
        </SchemaFormField>
      ))}
    </ViewContainer>
  );
}
