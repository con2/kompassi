import Link from "next/link";
import { notFound } from "next/navigation";

import SurveyEditorView from "../edit/SurveyEditorView";
import { updateSurveyDefaultDimensions } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query SurveyDimensionDefaults(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String!
  ) {
    event(slug: $eventSlug) {
      name
      slug

      forms {
        survey(slug: $surveySlug) {
          slug
          title(lang: $locale)
          purpose
          canRemove
          languages {
            language
          }
          dimensions {
            ...DimensionRowGroup
          }
          cachedDefaultDimensions
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
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.attributes.dimensions,
  });

  return { title };
}

export default async function SurveyDimensionDefaultsPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey?.dimensions) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const dimensions = data.event.forms.survey.dimensions;

  validateCachedDimensions(survey.cachedDefaultDimensions);

  return (
    <SurveyEditorView
      params={params}
      survey={survey}
      activeTab="dimensionDefaults"
    >
      <p className="form-text">{t.attributes.dimensionDefaults.description} </p>
      <DimensionValueSelectionForm
        dimensions={dimensions}
        cachedDimensions={survey.cachedDefaultDimensions}
        onChange={updateSurveyDefaultDimensions.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        translations={translations}
        technicalDimensions="readonly"
      />
      <p className="form-text mb-0">
        <Link
          className="link-subtle"
          href={`/${locale}/${eventSlug}/surveys/${surveySlug}/dimensions`}
          target="_blank"
        >
          {t.actions.editDimensions}…
        </Link>
      </p>
    </SurveyEditorView>
  );
}
