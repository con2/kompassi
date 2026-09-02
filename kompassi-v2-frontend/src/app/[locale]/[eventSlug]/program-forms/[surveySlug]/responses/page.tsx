import {
  Column,
  DataTable,
  DimensionFilters,
  FormattedDateTime,
  ModalButton,
  SignInRequired,
  UploadedFileLink,
} from "@con2/components";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { Fragment, ReactNode } from "react";

import { graphql } from "@/__generated__";
import {
  CanResponsesBeDeleted,
  ProgramFormResponseFragment,
  SurveyPurpose,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import {
  buildDimensionFilters,
  toFilterableDimensions,
} from "@/components/dimensions/helpers";
import { validateFields } from "@/components/forms/models";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import { kompassiBaseUrl } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import {
  deleteSurveyResponses,
  toggleSurveyResponseSubscription,
} from "../../../surveys/[surveySlug]/responses/actions";
import { ResponseListActions } from "../../../surveys/[surveySlug]/responses/ResponseListActions";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment ProgramFormResponse on LimitedResponseType {
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
  query ProgramFormResponses(
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
        survey(slug: $surveySlug, app: PROGRAM) {
          slug
          title(lang: $locale)
          purpose
          anonymity

          fields(lang: $locale, keyFieldsOnly: true)
          dimensions {
            ...DimensionFilter
            ...ColoredDimensionTableCell
          }

          countResponses
          responsesDeletionStatus

          responses(filters: $filters) {
            ...ProgramFormResponse
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
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
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

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.responseListTitle,
  });

  return { title };
}

export const revalidate = 0;

export default async function ProgramFormResponsesPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
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

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale, filters },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const survey = data.event.forms.survey;

  if (survey.purpose === SurveyPurpose.Default) {
    redirect(`/${eventSlug}/program-offers?form=${surveySlug}`);
  }

  const { anonymity } = survey;
  const anonymityMessages =
    translations.Survey.attributes.anonymity.thirdPerson;

  const dimensions = survey.dimensions ?? [];
  const listFilters = dimensions.filter((dimension) => dimension.isListFilter);
  const keyFields = survey.fields;
  validateFields(keyFields);

  const columns: Column<ProgramFormResponseFragment>[] = [
    {
      slug: "sequenceNumber",
      title: "#",
    },
    {
      slug: "revisionCreatedAt",
      title: t.attributes.originalCreatedAt,
      getCellContents: (row) => (
        <Link
          href={`/${eventSlug}/program-forms/${surveySlug}/responses/${row.id}`}
        >
          <FormattedDateTime value={row.revisionCreatedAt} locale={locale} />
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

  const canRemoveResponses =
    survey.responsesDeletionStatus === CanResponsesBeDeleted.Yes;

  // Program forms are protected by the event-wide program preferences toggle
  // rather than a per-survey one, so the message for that reason differs.
  const deletionStatusReasons = {
    ...t.actions.deleteVisibleResponses.reasons,
    NO_PROTECTED: translations.Program.ProgramForm.actions.responsesProtected,
  };

  const cannotRemoveResponsesReason: string | ReactNode | null =
    canRemoveResponses
      ? null
      : responses.length < 1
        ? t.actions.deleteVisibleResponses.noResponsesToDelete
        : deletionStatusReasons[survey.responsesDeletionStatus];

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programForms"
      searchParams={searchParams}
      actions={
        <ResponseListActions
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
              canRemoveResponses
                ? deleteSurveyResponses.bind(
                    null,
                    locale,
                    eventSlug,
                    surveySlug,
                    responses.map((response) => response.id),
                    searchParams,
                    `${eventSlug}/program-forms/${surveySlug}/responses`,
                  )
                : undefined
            }
            className="btn btn-outline-danger"
          >
            {canRemoveResponses
              ? t.actions.deleteVisibleResponses.confirmation(responses.length)
              : cannotRemoveResponsesReason}
          </ModalButton>
        </ResponseListActions>
      }
    >
      <h3 className="mt-4">
        {t.responseListTitle}: {survey.title}
      </h3>

      <DimensionFilters
        dimensions={toFilterableDimensions(listFilters)}
        locale={locale}
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
    </ProgramAdminView>
  );
}
