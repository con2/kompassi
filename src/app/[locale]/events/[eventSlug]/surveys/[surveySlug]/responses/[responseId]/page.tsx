import { notFound } from "next/navigation";

import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { SignInRequired } from "@/components/SignInRequired";

import { auth } from "@/auth";
import { defaultLayout, Field } from "@/components/SchemaForm/models";
import { SchemaFormResponse } from "@/components/SchemaForm/SchemaFormResponse";
import Link from "next/link";
import SchemaFormField from "@/components/SchemaForm/SchemaFormField";
import SchemaFormInput from "@/components/SchemaForm/SchemaFormInput";

const query = gql(`
  query EventSurveyResponseDetail($eventSlug:String!, $surveySlug:String!, $responseId:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          slug

          response(id: $responseId) {
            id
            createdAt
            language
            values

            form {
              fields
              layout
            }
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

  const t = translations.EventSurveyResponse;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.singleTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function EventSurveyResponsePage({ params }: Props) {
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired translations={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response?.form) {
    notFound();
  }

  const t = translations.EventSurveyResponse;

  const { createdAt, language, form } = data.event.forms.survey.response;
  const fields: Field[] = form.fields ?? [];
  const layout = form.layout ?? defaultLayout;
  const values: Record<string, any> =
    data.event.forms.survey.response.values ?? {};

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

  return (
    <main className="container mt-4">
      <Link
        className="link-subtle"
        href={`/events/${eventSlug}/surveys/${surveySlug}/responses`}
      >
        &lt; {t.returnToResponseList}
      </Link>

      <h1 className="mt-2 mb-4">
        {t.singleTitle}{" "}
        <span className="fs-5 text-muted">{data.event.forms.survey.title}</span>
      </h1>

      <SchemaFormField field={createdAtField} layout={layout}>
        <SchemaFormInput
          field={createdAtField}
          value={formattedCreatedAt}
          readOnly
        />
      </SchemaFormField>

      <SchemaFormField field={languageField} layout={layout}>
        <SchemaFormInput field={languageField} value={language} readOnly />
      </SchemaFormField>

      <SchemaFormResponse fields={fields} values={values} layout={layout} />
    </main>
  );
}
