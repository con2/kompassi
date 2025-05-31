import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";

import { graphql } from "@/__generated__";
import { ProgramOfferFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import ColoredDimensionTableCell, {
  buildKeyDimensionColumns,
} from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import {
  buildDimensionFilters,
  getDimensionValueTitle,
} from "@/components/dimensions/helpers";
import { Dimension } from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import UploadedFileLink from "@/components/forms/UploadedFileLink";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment ProgramOffer on FullResponseType {
    id
    createdAt
    createdBy {
      fullName
    }
    sequenceNumber
    values(keyFieldsOnly: true)
    form {
      survey {
        title(lang: $locale)
      }
      language
    }
    cachedDimensions
    programs {
      slug
      title
    }
  }
`);

graphql(`
  fragment ProgramOfferDimension on FullDimensionType {
    slug
    title(lang: $locale)
    isKeyDimension
    isTechnical

    values(lang: $locale) {
      slug
      title(lang: $locale)
      color
      isTechnical
    }
  }
`);

// TODO
const query = graphql(`
  query ProgramOffers(
    $eventSlug: String!
    $locale: String
    $filters: [DimensionFilterInput!]
  ) {
    event(slug: $eventSlug) {
      slug
      name
      program {
        programOffersExcelExportLink

        listFilters: dimensions(isListFilter: true, publicOnly: false) {
          ...ProgramOfferDimension
        }

        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {
          ...ProgramOfferDimension
        }

        stateDimension {
          ...ProgramOfferDimension
        }

        countProgramOffers
        programOffers(filters: $filters) {
          ...ProgramOffer
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
  searchParams: Record<string, string>;
}

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Program.ProgramOffer;

  // while dimension filters are not needed to form the title,
  // we would like to do only one query per request
  // so do the exact same query here so that it can be cached
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });

  if (!data.event?.program?.programOffers) {
    notFound();
  }

  const title = getPageTitle({
    viewTitle: t.listTitle,
    event: data.event,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ProgramOffersPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.ProgramOffer;
  const queryString = new URLSearchParams(searchParams).toString();
  const surveyT = translations.Survey;
  const programT = translations.Program;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });

  if (!data.event?.program?.programOffers) {
    notFound();
  }

  const event = data.event;

  const keyFields: Field[] = [
    {
      slug: "title",
      type: "SingleLineText",
      title: programT.attributes.title,
    },
  ];

  const columns: Column<ProgramOfferFragment>[] = [
    {
      slug: "createdAt",
      title: <>{surveyT.attributes.createdAt} 🔼</>,
      getCellContents: (row) => (
        <Link href={`/${eventSlug}/program-offers/${row.id}?${queryString}`}>
          <FormattedDateTime
            value={row.createdAt}
            locale={locale}
            scope={data.event}
            session={session}
          />
        </Link>
      ),
    },
    {
      slug: "createdBy",
      title: surveyT.attributes.createdBy,
      getCellContents: (row) => row.createdBy?.fullName || "",
    },
  ];

  // TODO encap (duplicated in SurveyResponsesPage)
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

  // Yoink the state dimension from key dimensions (it gets special treatment)
  const keyDimensions = data.event.program.keyDimensions.filter(
    (keyDimension) => keyDimension.slug !== "state",
  );
  columns.push(...buildKeyDimensionColumns(keyDimensions));

  const stateDimension = data.event.program.stateDimension;
  if (stateDimension) {
    columns.push({
      slug: "state",
      title: stateDimension.title,
      getCellElement: (row, children) => (
        <ColoredDimensionTableCell
          cachedDimensions={row.cachedDimensions}
          dimension={stateDimension}
        >
          {children}
        </ColoredDimensionTableCell>
      ),
      getCellContents: (row) => {
        // It's a rare occurrence that multiple programs are created from a single offer,
        // but as a quick workaround, if such is the case, make a link for each.
        if (row.programs.length > 0) {
          return row.programs.map((program) => (
            <div key={program.slug}>
              <Link
                className="link-subtle"
                href={`/${event.slug}/program-admin/${program.slug}`}
                title={program.title}
              >
                {getDimensionValueTitle(stateDimension, row.cachedDimensions)}
              </Link>
            </div>
          ));
        } else {
          return getDimensionValueTitle(stateDimension, row.cachedDimensions);
        }
      },
    });
  } else {
    // TODO is this fallback necessary?
    columns.push({
      slug: "state",
      title: programT.attributes.state.title,
      getCellContents: (row) => {
        if (row.programs.length > 0) {
          return row.programs.map((program) => (
            <div key={program.slug}>
              <Link
                className="link-subtle"
                href={`/${event.slug}/program-admin/${program.slug}`}
                title={program.title}
              >
                {programT.attributes.state.choices.accepted}
              </Link>
            </div>
          ));
        } else {
          return programT.attributes.state.choices.new;
        }
      },
    });
  }

  const programOffers = data.event.program.programOffers;
  const listFilters = data.event.program.listFilters;
  const excelExportLink = data.event.program.programOffersExcelExportLink
    ? `${data.event.program.programOffersExcelExportLink}?${queryString}`
    : null;

  // TODO ProgramAdminView
  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programOffers"
      searchParams={searchParams}
      actions={
        excelExportLink && (
          <a href={excelExportLink} className="btn btn-outline-primary">
            {surveyT.actions.exportDropdown.excel}
          </a>
        )
      }
    >
      <DimensionFilters
        dimensions={listFilters}
        className="row row-cols-md-auto g-3 align-items-center mb-4 mt-1 xxx-this-is-horrible"
      />
      <DataTable rows={programOffers} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {surveyT.showingResponses(
                programOffers.length,
                data.event.program.countProgramOffers,
              )}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminView>
  );
}
