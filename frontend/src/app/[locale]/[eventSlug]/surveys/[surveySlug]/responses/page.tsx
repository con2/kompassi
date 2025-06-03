import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment, ReactNode } from "react";

import {
  deleteSurveyResponses,
  toggleSurveyResponseSubscription,
} from "./actions";
import { ResponseListActions } from "./ResponseListActions";
import ResponseTabs from "./ResponseTabs";
import { graphql } from "@/__generated__";
import { SurveyResponseFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { validateFields } from "@/components/forms/models";
import UploadedFileLink from "@/components/forms/UploadedFileLink";
import ModalButton from "@/components/ModalButton";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment SurveyResponse on LimitedResponseType {
    id
    sequenceNumber
    revisionCreatedAt
    revisionCreatedBy {
      displayName
    }
    language
    values(keyFieldsOnly: true)
    cachedDimensions(keyDimensionsOnly: true)
  }
`);

const query = graphql(`
  query FormResponses(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
    $filters: [DimensionFilterInput!]
  ) {
    profile {
      forms {
        surveys(eventSlug: $eventSlug, relation: SUBSCRIBED) {
          slug
        }
      }
    }
    event(slug: $eventSlug) {
      name
      slug

      forms {
        survey(slug: $surveySlug) {
          slug
          title(lang: $locale)
          anonymity

          fields(lang: $locale, keyFieldsOnly: true)
          dimensions {
            slug
            title(lang: $locale)
            isKeyDimension

            values {
              slug
              title(lang: $locale)
              color
            }
          }

          countResponses
          canRemoveResponses
          protectResponses

          responses(filters: $filters) {
            ...SurveyResponse
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
  };
  searchParams: Record<string, string>;
}

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  // while dimension filters are not needed to form the title,
  // we would like to do only one query per request
  // so do the exact same query here so that it can be cached
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, filters },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.responseListTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function FormResponsesPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, filters },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const event = data.event;
  const survey = data.event.forms.survey;

  const { anonymity } = survey;
  const anonymityMessages =
    translations.Survey.attributes.anonymity.thirdPerson;

  const dimensions = survey.dimensions ?? [];
  const keyFields = survey.fields;
  validateFields(keyFields);

  const columns: Column<SurveyResponseFragment>[] = [
    {
      slug: "sequenceNumber",
      title: "#",
    },
    {
      slug: "revisionCreatedAt",
      title: t.attributes.originalCreatedAt,
      getCellContents: (row) => (
        <Link href={`/${eventSlug}/surveys/${surveySlug}/responses/${row.id}`}>
          <FormattedDateTime
            value={row.revisionCreatedAt}
            locale={locale}
            scope={data.event}
            session={session}
          />
        </Link>
      ),
    },
  ];

  if (anonymity === "NAME_AND_EMAIL") {
    columns.push({
      slug: "revisionCreatedBy",
      title: t.attributes.originalCreatedBy,
      getCellContents: (row) => row.revisionCreatedBy?.displayName || "",
    });
  }

  keyFields.forEach((keyField) => {
    columns.push({
      slug: `keyFields.${keyField.slug}`,
      title: keyField.summaryTitle ?? keyField.title ?? "",
      getCellContents(row) {
        // TODO move typing to codegen.ts (backend must specify scalar type)
        // TODO value types that need special processing? encap
        const values = row.values as Record<string, any>;
        const value = values[keyField.slug];

        if (keyField.type === "FileUpload") {
          // value is a list of presigned S3 URLs
          const urls: string[] = value ?? [];
          return urls.map((url, idx) => {
            return (
              <Fragment key={idx}>
                <UploadedFileLink url={url} />
                {idx !== urls.length - 1 && ", "}
              </Fragment>
            );
          });
        }

        return value;
      },
    });
  });

  columns.push(...buildKeyDimensionColumns(dimensions));

  const exportBaseUrl = `${kompassiBaseUrl}/events/${eventSlug}/surveys/${surveySlug}/responses`;
  const queryString = new URLSearchParams(searchParams).toString();
  const exportUrls = {
    excel: `${exportBaseUrl}.xlsx?${queryString}`,
    zip: `${exportBaseUrl}.zip?${queryString}`,
  };
  const responses = survey.responses || [];

  const subscribedSurveys = data.profile?.forms?.surveys ?? [];
  const isSubscribed = subscribedSurveys.some(
    (survey) => survey.slug === surveySlug,
  );

  let cannotRemoveResponsesReason: string | ReactNode | null = null;
  if (!survey.canRemoveResponses) {
    if (survey.protectResponses) {
      cannotRemoveResponsesReason =
        t.actions.deleteVisibleResponses.responsesProtected;
    } else if (responses.length < 1) {
      cannotRemoveResponsesReason =
        t.actions.deleteVisibleResponses.noResponsesToDelete;
    } else {
      cannotRemoveResponsesReason =
        t.actions.deleteVisibleResponses.cannotDelete;
    }
  }

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>

      <div className="d-flex align-items-middle">
        <ViewHeading>
          {t.responseListTitle}
          <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
        </ViewHeading>
        <div className="ms-auto">
          <ResponseListActions
            scope={event}
            survey={survey}
            isSubscribed={isSubscribed}
            onToggleSubscription={toggleSurveyResponseSubscription.bind(
              null,
              locale,
              eventSlug,
              surveySlug,
              !isSubscribed,
            )}
            exportUrls={exportUrls}
            messages={{
              toggleSubscription: t.actions.toggleSubscription,
              exportDropdown: t.actions.exportDropdown,
            }}
          >
            <ModalButton
              title={t.actions.deleteVisibleResponses.title}
              messages={t.actions.deleteVisibleResponses.modalActions}
              action={
                survey.canRemoveResponses
                  ? deleteSurveyResponses.bind(
                      null,
                      locale,
                      eventSlug,
                      surveySlug,
                      responses.map((response) => response.id),
                      searchParams,
                    )
                  : undefined
              }
              className="btn btn-outline-danger"
            >
              {survey.canRemoveResponses
                ? t.actions.deleteVisibleResponses.confirmation(
                    responses.length,
                  )
                : cannotRemoveResponsesReason}
            </ModalButton>
          </ResponseListActions>
        </div>
      </div>

      <DimensionFilters dimensions={dimensions} />
      <ResponseTabs
        eventSlug={eventSlug}
        surveySlug={surveySlug}
        searchParams={searchParams}
        active="responses"
        translations={translations}
      />

      <DataTable rows={responses} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.showingResponses(responses.length, survey.countResponses)}
            </td>
          </tr>
        </tfoot>
      </DataTable>

      <p>
        <small>
          <strong>{anonymityMessages.title}: </strong>
          {anonymityMessages.choices[anonymity]}
        </small>
      </p>
    </ViewContainer>
  );
}
