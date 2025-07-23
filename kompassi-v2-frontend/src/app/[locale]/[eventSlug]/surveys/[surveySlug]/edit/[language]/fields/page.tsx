import { notFound } from "next/navigation";

import SurveyEditorView from "../../SurveyEditorView";
import { promoteFieldToDimension, updateSurveyFields } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import FormEditorWrapper from "@/components/forms/FormEditorWrapper";
import { validateFields } from "@/components/forms/models";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment EditSurveyFieldsPage on FullSurveyType {
    slug
    title(lang: $locale)
    canRemove
    purpose

    dimensions {
      ...DimensionEditor
    }

    form(lang: $language) {
      title
      language
      fields(enrich: false)
      canRemove
    }

    languages {
      language
    }
  }
`);

const query = graphql(`
  query EditSurveyFieldsPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $language: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
          ...EditSurveyFieldsPage
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string; // UI language
    eventSlug: string;
    surveySlug: string;
    language: string; // language code of form being edited
  }>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug, language } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

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
}

export default async function EditSurveyLanguagePage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug, language } = params;
  const translations = getTranslations(locale);
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
  const activeTab = `fields-${language}`;
  const dimensions = data.event.forms.survey.dimensions;

  validateFields(form.fields);

  return (
    <SurveyEditorView params={params} survey={survey} activeTab={activeTab}>
      <FormEditorWrapper
        initialFields={form.fields}
        dimensions={dimensions}
        messages={{
          FormEditor: translations.FormEditor,
          SchemaForm: translations.SchemaForm,
        }}
        onChange={updateSurveyFields.bind(
          null,
          eventSlug,
          surveySlug,
          language,
        )}
        onPromoteFieldToDimension={promoteFieldToDimension.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
      />
    </SurveyEditorView>
  );
}
