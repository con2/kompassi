import Link from "next/link";
import { notFound } from "next/navigation";

import { ReactNode } from "react";
import { deleteSurveyResponses } from "../actions";
import { updateResponseDimensions } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import AutoSubmitForm from "@/components/AutoSubmitForm";
import { buildDimensionValueSelectionForm } from "@/components/dimensions/DimensionValueSelectionForm";
import { validateCachedDimensions } from "@/components/dimensions/models";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query SurveyResponseDetail(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          slug
          anonymity
          canRemoveResponses
          protectResponses

          dimensions {
            title(lang: $locale)
            slug
            isTechnical
            isMultiValue

            values {
              title(lang: $locale)
              slug
              color
            }
          }

          response(id: $responseId) {
            id
            sequenceNumber
            createdAt
            createdBy {
              displayName
              email
            }
            language
            values
            form {
              fields
            }
            cachedDimensions
          }
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
    responseId: string;
  };
}

export async function generateMetadata({ params }: Props) {
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

export default async function SurveyResponsePage({ params }: Props) {
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, responseId },
  });

  if (!data.event?.forms?.survey?.response?.form) {
    notFound();
  }

  const t = translations.Survey;

  const { anonymity, canRemoveResponses, protectResponses } =
    data.event.forms.survey;
  const { sequenceNumber, createdAt, language, form } =
    data.event.forms.survey.response;
  const { fields } = form;

  const response = data.event.forms.survey.response;
  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  // TODO using synthetic form fields for presentation is a hack
  // but it shall suffice until someone comes up with a Design Vision™
  const technicalFields: Field[] = [
    {
      slug: "sequenceNumber",
      type: "SingleLineText",
      title: t.attributes.sequenceNumber,
    },
    {
      slug: "createdAt",
      // TODO(#438) use DateTimeField
      type: "SingleLineText",
      title: t.attributes.createdAt,
    },
  ];

  if (anonymity === "NAME_AND_EMAIL") {
    technicalFields.push({
      slug: "createdBy",
      type: "SingleLineText",
      title: t.attributes.createdBy,
    });
  }

  // TODO(#438) use DateTimeField
  const formattedCreatedAt = createdAt ? formatDateTime(createdAt, locale) : "";
  const createdBy = response.createdBy;
  const formattedCreatedBy = createdBy
    ? `${createdBy.displayName} <${createdBy.email}>`
    : "-";

  const technicalValues = {
    sequenceNumber,
    createdAt: formattedCreatedAt,
    createdBy: formattedCreatedBy,
  };

  const dimensions = data.event.forms.survey.dimensions ?? [];

  validateCachedDimensions(response.cachedDimensions);
  const { fields: dimensionFields, values: dimensionValues } =
    buildDimensionValueSelectionForm(dimensions, response.cachedDimensions);

  let cannotRemoveReason: string | ReactNode | null = null;
  if (!canRemoveResponses) {
    if (protectResponses) {
      cannotRemoveReason = t.actions.deleteVisibleResponses.responsesProtected;
    } else {
      cannotRemoveReason = t.actions.deleteResponse.cannotDelete;
    }
  }

  return (
    <ViewContainer>
      <Link
        className="link-subtle"
        href={`/${eventSlug}/surveys/${surveySlug}/responses`}
      >
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.responseDetailTitle}
          <ViewHeading.Sub>{data.event.forms.survey.title}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.deleteResponse.title}
            messages={t.actions.deleteResponse.modalActions}
            action={
              canRemoveResponses
                ? deleteSurveyResponses.bind(
                    null,
                    locale,
                    eventSlug,
                    surveySlug,
                    [response.id],
                    {},
                  )
                : undefined
            }
            className="btn btn-outline-danger"
          >
            {canRemoveResponses
              ? t.actions.deleteResponse.confirmation
              : cannotRemoveReason}
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <div className="row mb-5">
        {!!dimensions?.length && (
          <div className="col-md-8">
            <div className="card mb-3 h-100">
              <div className="card-body">
                <h5 className="card-title mb-3">{t.attributes.dimensions}</h5>
                {/* TODO improve feedback of successful save */}
                <AutoSubmitForm
                  action={updateResponseDimensions.bind(
                    null,
                    eventSlug,
                    surveySlug,
                    responseId,
                  )}
                >
                  <SchemaForm
                    fields={dimensionFields}
                    values={dimensionValues}
                    messages={translations.SchemaForm}
                  />
                  <noscript>
                    <SubmitButton>{t.actions.saveDimensions}</SubmitButton>
                  </noscript>
                </AutoSubmitForm>
              </div>
            </div>
          </div>
        )}
        <div className="col">
          <div className="card mb-3 h-100">
            <div className="card-body">
              <h5 className="card-title mb-3">
                {t.attributes.technicalDetails}
              </h5>
              <SchemaForm
                fields={technicalFields}
                values={technicalValues}
                messages={translations.SchemaForm}
                readOnly
              />
            </div>
          </div>
        </div>
      </div>

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ViewContainer>
  );
}
