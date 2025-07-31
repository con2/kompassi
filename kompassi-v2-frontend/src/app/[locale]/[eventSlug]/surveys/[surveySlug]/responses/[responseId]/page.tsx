import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionValueSelectionForm, {
  buildDimensionValueSelectionForm,
} from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import { getTranslations } from "@/translations";
import { updateResponseDimensions } from "./actions";
import { OldVersionAlert } from "@/components/response/OldVersionAlert";
import ResponseHistorySidebar from "@/components/response/ResponseHistorySidebar";
import SurveyResponseAdminView from "@/components/response/SurveyResponseAdminView";
import { ButtonGroup } from "react-bootstrap";
import ModalButton from "@/components/ModalButton";
import { deleteSurveyResponses } from "../actions";

graphql(`
  fragment SurveyResponseDetail on FullResponseType {
    ...ResponseHistorySidebar

    values
    cachedDimensions

    form {
      description
      fields
      survey {
        title(lang: $locale)
        slug
        cachedDefaultResponseDimensions
        cachedDefaultInvolvementDimensions
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
  query SurveyResponseDetail(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      slug
      name
      timezone

      involvement {
        dimensions(publicOnly: false) {
          ...DimensionValueSelect
        }
      }

      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          slug
          anonymity
          canRemoveResponses
          protectResponses

          dimensions(publicOnly: false) {
            ...DimensionValueSelect
          }

          response(id: $responseId) {
            ...SurveyResponseDetail
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

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.responseDetailTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function SurveyResponsePage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, responseId, surveySlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, responseId, surveySlug },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const t = translations.Survey;

  const response = data.event?.forms?.survey?.response;
  const { event } = data;
  const { form, supersededBy, canEdit } = response;
  const { fields, survey } = form;

  const values: Record<string, any> = response.values ?? {};
  const { canDelete } = response;

  validateFields(fields);

  validateCachedDimensions(response.cachedDimensions);
  const surveyDimensions = data.event.forms.survey.dimensions;
  const defaultSurveyDimensions =
    response.form.survey.cachedDefaultResponseDimensions ?? {};
  validateCachedDimensions(defaultSurveyDimensions);
  const dimensionsReadOnly = !!supersededBy;

  return (
    <SurveyResponseAdminView
      translations={translations}
      event={data.event}
      searchParams={searchParams}
      survey={survey}
      actions={
        <ButtonGroup>
          <ModalButton
            className="btn btn-outline-danger"
            label={t.actions.deleteResponse.label + "…"}
            title={t.actions.deleteResponse.title}
            messages={t.actions.deleteResponse.modalActions}
            disabled={!canDelete}
            action={deleteSurveyResponses.bind(
              null,
              locale,
              eventSlug,
              surveySlug,
              [responseId],
              searchParams,
            )}
          >
            {t.actions.deleteResponse.confirmation}
          </ModalButton>

          <Link
            className={`btn btn-outline-primary ${canEdit ? "" : "disabled"}`}
            href={`/${locale}/${eventSlug}/surveys/${surveySlug}/responses/${responseId}/edit`}
            title={t.actions.editResponse.title}
          >
            {t.actions.editResponse.label}
          </Link>
        </ButtonGroup>
      }
    >
      {supersededBy ? (
        <OldVersionAlert
          supersededBy={supersededBy}
          basePath={`/${eventSlug}/program-offers`}
          messages={t.OldVersionAlert}
          className="mt-4 mb-4"
        />
      ) : (
        <>
          <div className="row mb-5 mt-4">
            {!!surveyDimensions?.length && (
              <div className="col-md-8">
                <div className="card mb-3 h-100">
                  <div className="card-body">
                    <h5 className="card-title mb-3">
                      {t.attributes.dimensions}
                    </h5>
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
                responsesBaseUrl={`/${event.slug}/surveys/${surveySlug}/responses`}
                session={session}
                messages={translations}
              />
            </div>
          </div>
        </>
      )}

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </SurveyResponseAdminView>
  );
}
