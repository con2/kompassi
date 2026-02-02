import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";

import { graphql } from "@/__generated__";
import { ProgramFormResponseFragment } from "@/__generated__/graphql";
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
import ProgramAdminView from "@/components/program/ProgramAdminView";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";
import ExportDropdown from "../../../surveys/[surveySlug]/responses/ExportDropdown";

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

    programs {
      slug
      title
    }
  }
`);

const query = graphql(`
  query ProgramFormResponses(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
    $filters: [DimensionFilterInput!]
  ) {
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
            ...DimensionFilter
            ...ColoredDimensionTableCell
          }

          countResponses
          canRemoveResponses
          protectResponses

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

  return {
    title: `${data.event.name}: ${data.event.forms.survey.title} (${t.responseListTitle}) – Kompassi`,
  };
}

export const revalidate = 0;

export default async function ProgramFormResponsesPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const programT = translations.Program;
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

  columns.push({
    slug: "revisionCreatedBy",
    title: t.attributes.originalCreatedBy,
    getCellContents: (row) => row.revisionCreatedBy?.displayName || "",
  });

  columns.push({
    slug: "program",
    title: programT.singleTitle,
    getCellContents(row) {
      return row.programs.map((program) => (
        <div key={program.slug}>
          <Link
            href={`/${eventSlug}/program-admin/${program.slug}`}
            className="link-subtle"
          >
            {program.title}
          </Link>
        </div>
      ));
    },
  });

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

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programForms"
      searchParams={{}} // Program dimension filters do not apply to program forms
      actions={
        <ExportDropdown
          messages={translations.Survey.actions.exportDropdown}
          exportUrls={exportUrls}
        />
      }
    >
      <h3 className="mt-3 mb-2">
        {t.responseListTitle}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </h3>

      {/* TODO implement filtering once the responses are in the involvement universe */}
      {/* <DimensionFilters dimensions={listFilters} /> */}

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
