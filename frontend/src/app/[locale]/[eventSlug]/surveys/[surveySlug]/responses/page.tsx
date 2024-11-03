import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";

import { toggleSurveyResponseSubscription } from "./actions";
import ResponseTabs from "./ResponseTabs";
import SubscriptionButton from "./SubscriptionButton";
import { graphql } from "@/__generated__";
import { SurveyResponseFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import ColoredDimensionTableCell from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import {
  buildDimensionFilters,
  getDimensionValueTitle,
} from "@/components/dimensions/helpers";
import FormattedDateTime from "@/components/FormattedDateTime";
import { validateFields } from "@/components/forms/models";
import UploadedFileLink from "@/components/forms/UploadedFileLink";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment SurveyResponse on LimitedResponseType {
    id
    sequenceNumber
    createdAt
    createdBy {
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
        surveys(eventSlug: $eventSlug) {
          slug
        }
      }
    }
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug) {
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
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (row) => (
        <Link href={`/${eventSlug}/surveys/${surveySlug}/responses/${row.id}`}>
          <FormattedDateTime
            value={row.createdAt}
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
      slug: "createdBy",
      title: t.attributes.createdBy,
      getCellContents: (row) => row.createdBy?.displayName || "",
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

  dimensions
    .filter((dimension) => dimension.isKeyDimension)
    .forEach((keyDimension) => {
      columns.push({
        slug: `keyDimensions.${keyDimension.slug}`,
        title: keyDimension.title ?? "",
        getCellElement: (row, children) => (
          <ColoredDimensionTableCell
            cachedDimensions={row.cachedDimensions}
            dimension={keyDimension}
          >
            {children}
          </ColoredDimensionTableCell>
        ),
        getCellContents: (row) =>
          getDimensionValueTitle(keyDimension, row.cachedDimensions),
      });
    });

  const excelUrl = `${kompassiBaseUrl}/events/${eventSlug}/surveys/${surveySlug}/responses.xlsx`;
  const responses = survey.responses || [];

  const subscribedSurveys = data.profile?.forms?.surveys ?? [];
  const isSubscribed = subscribedSurveys.some(
    (survey) => survey.slug === surveySlug,
  );

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
          <div className="btn-group">
            <SubscriptionButton
              initialChecked={isSubscribed}
              onChange={toggleSurveyResponseSubscription.bind(
                null,
                locale,
                eventSlug,
                surveySlug,
              )}
            >
              {t.actions.toggleSubscription}
            </SubscriptionButton>
            <a className="btn btn-outline-primary" href={excelUrl}>
              {t.actions.downloadAsExcel}…
            </a>
          </div>
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

      <p className="mt-3">
        {t.showingResponses(responses.length, survey.countResponses)}
      </p>
      <DataTable rows={responses} columns={columns} />

      <p>
        <small>
          <strong>{anonymityMessages.title}: </strong>
          {anonymityMessages.choices[anonymity]}
        </small>
      </p>
    </ViewContainer>
  );
}
