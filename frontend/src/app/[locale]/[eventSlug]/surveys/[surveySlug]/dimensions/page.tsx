import { notFound } from "next/navigation";

import SurveyEditorView from "../edit/SurveyEditorView";
import {
  createDimension,
  createDimensionValue,
  deleteDimension,
  deleteDimensionValue,
  reorderDimensions,
  reorderDimensionValues,
  updateDimension,
  updateDimensionValue,
} from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionEditor } from "@/components/dimensions/DimensionEditor";
import SignInRequired from "@/components/errors/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query DimensionsList(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String!
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          slug
          title(lang: $locale)
          canRemove
          purpose
          languages {
            language
          }
          dimensions {
            ...DimensionEditor
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    surveySlug: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
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

export default async function SurveyDimensionsPage(props: Props) {
  const params = await props.params;
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

  return (
    <SurveyEditorView params={params} survey={survey} activeTab="dimensions">
      <DimensionEditor
        dimensions={dimensions}
        translations={translations}
        onCreateDimension={createDimension.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onUpdateDimension={updateDimension.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onDeleteDimension={deleteDimension.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onReorderDimensions={reorderDimensions.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onCreateDimensionValue={createDimensionValue.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onUpdateDimensionValue={updateDimensionValue.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onDeleteDimensionValue={deleteDimensionValue.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
        onReorderDimensionValues={reorderDimensionValues.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
        )}
      />
    </SurveyEditorView>
  );
}
