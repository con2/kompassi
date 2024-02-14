import { notFound } from "next/navigation";

import SurveyEditorView from "../SurveyEditorView";
import { updateForm } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { getPropertiesFormFields } from "@/components/forms/getPropertiesFormFields";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment EditSurveyLanguagePage on SurveyType {
    slug
    title(lang: $locale)
    canRemove

    form(lang: $language) {
      title
      description
      thankYouMessage
      fields
      canRemove
    }

    languages {
      language
    }
  }
`);

const query = graphql(`
  query EditSurveyLanguagePageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $language: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          ...EditSurveyLanguagePage
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string; // UI language
    eventSlug: string;
    surveySlug: string;
    language: string; // language code of form being edited
  };
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug, language } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  try {
    const { data } = await getClient().query({
      query,
      variables: { locale, eventSlug, surveySlug, language },
    });

    if (!data.event?.forms?.survey?.form) {
      notFound();
    }

    const title = getPageTitle({
      translations,
      event: data.event,
      subject: data.event.forms.survey.form.title,
      viewTitle: t.editSurveyPage.title,
    });

    return { title };
  } catch (e) {
    console.log(JSON.stringify(e, null, 2));
  }
}

export default async function EditSurveyPage({ params }: Props) {
  const { locale, eventSlug, surveySlug, language } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug, language },
  });

  if (!data?.event?.forms?.survey?.form) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const form = data.event.forms.survey.form;

  const fields: Field[] = getPropertiesFormFields(
    translations.FormEditor.formPropertiesForm,
  );

  return (
    <SurveyEditorView params={params} survey={survey} activeTab={language}>
      <form action={updateForm.bind(null, eventSlug, surveySlug, language)}>
        <SchemaForm
          fields={fields}
          values={form}
          messages={translations.SchemaForm}
        />
        <SubmitButton>{t.actions.saveProperties}</SubmitButton>
      </form>
    </SurveyEditorView>
  );
}
