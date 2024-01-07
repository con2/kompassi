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
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";

const query = gql(`
  query OwnResponseDetail($responseId: String!) {
    profile {
      forms {
        response(id: $responseId) {
          id
          createdAt
          values
          form {
            slug
            title
            language
            fields
            layout
            event {
              slug
              name
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
    responseId: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.SurveyResponse;

  return {
    title: `${t.ownResponses} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function SurveyResponsePage({ params }: Props) {
  const { locale, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { responseId },
  });

  if (!data.profile?.forms?.response) {
    notFound();
  }

  const t = translations.SurveyResponse;

  const response = data.profile.forms.response;
  const { createdAt, form } = response;
  const language = form.language;
  const fields: Field[] = form.fields ?? [];
  const layout = form.layout ?? defaultLayout;
  const values: Record<string, any> = response.values ?? {};

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
    <ViewContainer>
      <Link className="link-subtle" href={`/profile/responses`}>
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeading>
        {t.singleTitle}
        <ViewHeading.Sub>{form.title}</ViewHeading.Sub>
      </ViewHeading>

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
    </ViewContainer>
  );
}
