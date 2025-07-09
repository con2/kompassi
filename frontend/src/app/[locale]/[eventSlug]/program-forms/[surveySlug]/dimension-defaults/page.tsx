import Link from "next/link";
import { notFound } from "next/navigation";

import ProgramFormEditorView from "../edit/ProgramFormEditorView";
import { updateProgramFormDefaultDimensions } from "./actions";
import { graphql } from "@/__generated__";
import {
  SurveyDefaultDimensionsUniverse,
  SurveyPurpose,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
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

      involvement {
        dimensions(publicOnly: false) {
          ...DimensionValueSelect
        }
      }

      forms {
        survey(slug: $surveySlug, app: PROGRAM_V2) {
          slug
          title(lang: $locale)
          canRemove
          purpose
          languages {
            language
          }
          dimensions(publicOnly: false) {
            ...DimensionValueSelect
          }
          cachedDefaultResponseDimensions
          cachedDefaultInvolvementDimensions
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

  const surveyT = translations.Survey;
  const t = translations.Program.ProgramForm;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey?.dimensions) {
    notFound();
  }

  const event = data.event;
  const survey = data.event.forms.survey;
  const programDimensions = data.event.forms.survey.dimensions;
  const involvementDimensions = data.event.involvement?.dimensions ?? [];

  validateCachedDimensions(survey.cachedDefaultResponseDimensions);
  validateCachedDimensions(survey.cachedDefaultInvolvementDimensions);

  return (
    <ProgramFormEditorView
      event={event}
      survey={survey}
      activeTab="dimensionDefaults"
      translations={translations}
    >
      <h4>{t.attributes.involvementDimensionDefaults.title}</h4>
      <p className="form-text">
        {t.attributes.involvementDimensionDefaults.description}{" "}
        <Link
          className="link-subtle"
          href={`/${eventSlug}/involvement-dimensions`}
          target="_blank"
        >
          {surveyT.actions.editDimensions}…
        </Link>
      </p>
      <DimensionValueSelectionForm
        dimensions={involvementDimensions}
        cachedDimensions={survey.cachedDefaultInvolvementDimensions}
        onChange={updateProgramFormDefaultDimensions.bind(
          null,
          locale,
          eventSlug,
          surveySlug,
          SurveyDefaultDimensionsUniverse.Involvement,
        )}
        translations={translations}
        technicalDimensions="readonly"
        idPrefix="involvement-dimension-defaults"
      />

      {survey.purpose == SurveyPurpose.Default && (
        <>
          <h4>{t.attributes.programDimensionDefaults.title}</h4>
          <p className="form-text">
            {t.attributes.programDimensionDefaults.description}{" "}
            <Link
              className="link-subtle"
              href={`/${eventSlug}/program-dimensions`}
              target="_blank"
            >
              {surveyT.actions.editDimensions}…
            </Link>
          </p>
          <DimensionValueSelectionForm
            dimensions={programDimensions}
            cachedDimensions={survey.cachedDefaultResponseDimensions}
            onChange={updateProgramFormDefaultDimensions.bind(
              null,
              locale,
              eventSlug,
              surveySlug,
              SurveyDefaultDimensionsUniverse.Response,
            )}
            translations={translations}
            technicalDimensions="readonly"
            idPrefix="program-dimension-defaults"
          />
        </>
      )}
      <p className="form-text">
        {
          surveyT.attributes.dimensionDefaults
            .technicalDimensionsCannotBeChanged
        }
      </p>
    </ProgramFormEditorView>
  );
}
