import { notFound } from "next/navigation";

import { updateProgramForm } from "./actions";
import ProgramFormEditorView from "./ProgramFormEditorView";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment EditProgramForm on SurveyType {
    slug
    title(lang: $locale)
    activeFrom
    activeUntil
    canRemove

    languages {
      title
      language
      canRemove
    }
  }
`);

const query = graphql(`
  query EditProgramFormPage(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug

      forms {
        survey(slug: $surveySlug, app: PROGRAM_V2) {
          ...EditProgramForm
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
  };
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.editSurveyPage.title,
  });

  return { title };
}

export default async function EditSurveyPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data?.event?.forms?.survey) {
    notFound();
  }

  const survey = data?.event?.forms?.survey;

  const fields: Field[] = [
    {
      slug: "activeFrom",
      type: "DateTimeField",
      ...t.attributes.activeFrom,
    },
    {
      slug: "activeUntil",
      type: "DateTimeField",
      ...t.attributes.activeUntil,
    },
  ];

  return (
    <ProgramFormEditorView
      translations={translations}
      event={data.event}
      survey={survey}
      activeTab="properties"
    >
      <form action={updateProgramForm.bind(null, eventSlug, surveySlug)}>
        <SchemaForm
          fields={fields}
          values={survey}
          messages={translations.SchemaForm}
        />
        <SubmitButton>{t.actions.saveProperties}</SubmitButton>
      </form>
    </ProgramFormEditorView>
  );
}
