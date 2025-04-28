import Link from "next/link";
import { notFound } from "next/navigation";

import ProgramFormEditorView from "../edit/ProgramFormEditorView";
import { updateProgramFormDefaultDimensions } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query DimensionDefaults(
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

export default async function ProgramFormDimensionDefaults({ params }: Props) {
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

  const event = data.event;
  const survey = data.event.forms.survey;
  const dimensions = data.event.forms.survey.dimensions;

  validateCachedDimensions(survey.cachedDefaultDimensions);

  return (
    <ProgramFormEditorView
      event={event}
      survey={survey}
      activeTab="dimensionDefaults"
      translations={translations}
    >
      <p className="form-text">{t.attributes.dimensionDefaults.description} </p>
      <DimensionValueSelectionForm
        dimensions={dimensions}
        cachedDimensions={survey.cachedDefaultDimensions}
        onChange={updateProgramFormDefaultDimensions.bind(
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
          href={`/${locale}/${eventSlug}/program-dimensions`}
          target="_blank"
        >
          {t.actions.editDimensions}…
        </Link>
      </p>
    </ProgramFormEditorView>
  );
}
