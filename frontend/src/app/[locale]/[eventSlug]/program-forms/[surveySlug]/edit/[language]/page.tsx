import { notFound } from "next/navigation";

import ModalButton from "../../../../../../../components/ModalButton";
import ProgramFormEditorView from "../ProgramFormEditorView";
import {
  deleteProgramFormLanguage,
  updateProgramFormLanguage,
} from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment EditProgramFormLanguage on FullSurveyType {
    slug
    title(lang: $locale)
    canRemove
    purpose

    form(lang: $language) {
      title
      language
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
  query EditProgramFormLanguagePage(
    $eventSlug: String!
    $surveySlug: String!
    $language: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug

      forms {
        survey(slug: $surveySlug, app: PROGRAM_V2) {
          ...EditProgramFormLanguage
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

export default async function EditProgramFormLanguagePage(props: Props) {
  const params = await props.params;
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

  const rows = 3;
  const fields: Field[] = [
    {
      slug: "title",
      type: "SingleLineText",
      ...translations.FormEditor.attributes.title,
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows,
      ...translations.FormEditor.attributes.description,
    },
    {
      slug: "thankYouMessage",
      type: "MultiLineText",
      rows,
      ...translations.FormEditor.attributes.thankYouMessage,
    },
  ];

  const supportedLanguages: Record<string, string> =
    translations.LanguageSwitcher.supportedLanguages;
  const languageName = supportedLanguages[language] ?? form.language;
  const activeTab = `texts-${language}`;

  return (
    <ProgramFormEditorView
      translations={translations}
      event={data.event}
      survey={survey}
      activeTab={activeTab}
    >
      <form
        action={updateProgramFormLanguage.bind(
          null,
          eventSlug,
          surveySlug,
          language,
        )}
      >
        <SchemaForm
          fields={fields}
          values={form}
          messages={translations.SchemaForm}
        />
        <div className="d-flex">
          <SubmitButton>{t.actions.saveProperties}</SubmitButton>
          <ModalButton
            className="btn btn-outline-danger ms-auto"
            title={t.deleteLanguageModal.title}
            messages={t.deleteLanguageModal.modalActions}
            action={deleteProgramFormLanguage.bind(
              null,
              eventSlug,
              survey.slug,
              language,
            )}
            submitButtonVariant="danger"
            disabled={!form.canRemove}
          >
            {t.deleteLanguageModal.confirmation(languageName)}
          </ModalButton>
        </div>
      </form>
    </ProgramFormEditorView>
  );
}
