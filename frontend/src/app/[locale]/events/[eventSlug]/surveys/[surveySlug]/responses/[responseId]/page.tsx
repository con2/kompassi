import Link from "next/link";
import { notFound } from "next/navigation";

import { updateResponseDimensions } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import AutoSubmitForm from "@/components/AutoSubmitForm";
import { buildDimensionForm } from "@/components/dimensions/helpers";
import { SchemaForm } from "@/components/SchemaForm";
import { Field, validateFields } from "@/components/SchemaForm/models";
import SchemaFormField from "@/components/SchemaForm/SchemaFormField";
import SchemaFormInput from "@/components/SchemaForm/SchemaFormInput";
import { SchemaFormResponse } from "@/components/SchemaForm/SchemaFormResponse";
import SubmitButton from "@/components/SchemaForm/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query SurveyResponseDetail(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          slug
          anonymity
          dimensions {
            title(lang: $locale)
            slug
            isMultiValue
            values {
              title(lang: $locale)
              slug
              color
            }
          }
          response(id: $responseId) {
            id
            createdAt
            createdBy {
              displayName
              email
            }
            language
            values
            form {
              fields
              layout
            }
            cachedDimensions
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
    responseId: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.responseDetailTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function SurveyResponsePage({ params }: Props) {
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response?.form) {
    notFound();
  }

  const t = translations.Survey;

  const { anonymity } = data.event.forms.survey;
  const { createdAt, language, form } = data.event.forms.survey.response;
  const { fields, layout } = form;

  const response = data.event.forms.survey.response;
  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  // TODO using synthetic form fields for presentation is a hack
  // but it shall suffice until someone comes up with a Design Vision™
  const createdAtField: Field = {
    slug: "createdAt",
    type: "SingleLineText",
    title: t.attributes.createdAt,
  };
  const formattedCreatedAt = createdAt
    ? new Date(createdAt).toLocaleString(locale)
    : "";

  const languageField: Field = {
    slug: "language",
    type: "SingleLineText",
    title: t.attributes.language,
  };

  const createdByField: Field | undefined =
    anonymity == "NAME_AND_EMAIL"
      ? {
          slug: "createdBy",
          type: "SingleLineText",
          title: t.attributes.createdBy,
        }
      : undefined;

  const createdBy = response.createdBy;
  const formattedCreatedBy = createdBy
    ? `${createdBy.displayName} <${createdBy.email}>`
    : "-";

  const dimensions = data.event.forms.survey.dimensions ?? [];

  const { fields: dimensionFields, values: dimensionValues } =
    buildDimensionForm(dimensions, response.cachedDimensions);

  return (
    <ViewContainer>
      <Link
        className="link-subtle"
        href={`/events/${eventSlug}/surveys/${surveySlug}/responses`}
      >
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeading>
        {t.responseDetailTitle}
        <ViewHeading.Sub>{data.event.forms.survey.title}</ViewHeading.Sub>
      </ViewHeading>

      <div className="row mb-5">
        {!!dimensions?.length && (
          <div className="col-md-8">
            <div className="card mb-3 h-100">
              <div className="card-body">
                <h5 className="card-title mb-3">{t.attributes.dimensions}</h5>
                {/* TODO improve feedback of successful save */}
                <AutoSubmitForm
                  action={updateResponseDimensions.bind(
                    null,
                    eventSlug,
                    surveySlug,
                    responseId,
                  )}
                >
                  <SchemaForm
                    fields={dimensionFields}
                    values={dimensionValues}
                    messages={translations.SchemaForm}
                  />
                  <noscript>
                    <SubmitButton>{t.actions.saveDimensions}</SubmitButton>
                  </noscript>
                </AutoSubmitForm>
              </div>
            </div>
          </div>
        )}
        <div className="col">
          <div className="card mb-3 h-100">
            <div className="card-body">
              <h5 className="card-title mb-3">
                {t.attributes.technicalDetails}
              </h5>
              {createdByField && (
                <SchemaFormField field={createdByField} layout={layout}>
                  <SchemaFormInput
                    field={createdByField}
                    value={formattedCreatedBy}
                    messages={translations.SchemaForm}
                    readOnly
                  />
                </SchemaFormField>
              )}

              <SchemaFormField field={createdAtField} layout={layout}>
                <SchemaFormInput
                  field={createdAtField}
                  value={formattedCreatedAt}
                  messages={translations.SchemaForm}
                  readOnly
                />
              </SchemaFormField>
            </div>
          </div>
        </div>
      </div>

      <SchemaFormResponse
        fields={fields}
        values={values}
        layout={layout}
        messages={translations.SchemaForm}
      />
    </ViewContainer>
  );
}
