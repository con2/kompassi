import { SignInRequired } from "@con2/components";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { updateResponseDimensions } from "../../../../surveys/[surveySlug]/responses/[responseId]/actions";
import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import { OldVersionAlert } from "@/components/response/OldVersionAlert";
import ResponseHistorySidebar from "@/components/response/ResponseHistorySidebar";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramFormResponseDetail on FullResponseType {
    ...ResponseHistorySidebar

    values
    cachedDimensions

    form {
      description
      fields
      survey {
        title(lang: $locale)
        slug
        profileFieldSelector {
          ...FullProfileFieldSelector
        }
      }
    }

    canEdit(mode: ADMIN)
    canAccept
    canCancel
    canDelete
  }
`);

const query = graphql(`
  query ProgramFormResponseDetail(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      slug
      name
      timezone

      forms {
        survey(slug: $surveySlug, app: PROGRAM) {
          title(lang: $locale)
          slug
          purpose

          dimensions(publicOnly: false) {
            ...DimensionValueSelect
          }

          response(id: $responseId) {
            ...ProgramFormResponseDetail
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
    responseId: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.responseDetailTitle,
  });

  return { title };
}

export const revalidate = 0;

export default async function ProgramFormResponsePage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, responseId, surveySlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, responseId, surveySlug },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const survey = data.event.forms.survey;

  if (survey.purpose === SurveyPurpose.Default) {
    redirect(`/${eventSlug}/program-offers/${responseId}`);
  }

  const response = survey.response;
  if (!response) {
    notFound();
  }

  const t = translations.Survey;

  const { event } = data;
  const { form, supersededBy } = response;
  const { fields } = form;

  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  validateCachedDimensions(response.cachedDimensions);
  const surveyDimensions = survey.dimensions;
  const dimensionsReadOnly = !!supersededBy;

  const responsesBaseUrl = `/${eventSlug}/program-forms/${surveySlug}/responses`;

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programForms"
      searchParams={searchParams}
    >
      <Link className="link-subtle" href={responsesBaseUrl}>
        &lt; {t.responseListTitle}
      </Link>

      <h3 className="mt-4">
        {t.responseDetailTitle}: {survey.title}
      </h3>

      {supersededBy ? (
        <OldVersionAlert
          supersededBy={supersededBy}
          basePath={responsesBaseUrl}
          messages={t.OldVersionAlert}
          className="mt-4 mb-4"
        />
      ) : (
        <div className="row mb-5 mt-4">
          {!!surveyDimensions?.length && (
            <div className="col-md-8">
              <div className="card mb-3 h-100">
                <div className="card-body">
                  <h5 className="card-title mb-3">{t.attributes.dimensions}</h5>
                  <DimensionValueSelectionForm
                    dimensions={surveyDimensions}
                    cachedDimensions={response.cachedDimensions}
                    translations={translations}
                    technicalDimensions="readonly"
                    readOnly={dimensionsReadOnly}
                    idPrefix="response-dimensions"
                    onChange={updateResponseDimensions.bind(
                      null,
                      eventSlug,
                      surveySlug,
                      responseId,
                    )}
                  />
                </div>
              </div>
            </div>
          )}
          <div className="col">
            <ResponseHistorySidebar
              event={event}
              response={response}
              locale={locale}
              responsesBaseUrl={responsesBaseUrl}
              session={session}
              messages={translations}
            />
          </div>
        </div>
      )}

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ProgramAdminView>
  );
}
