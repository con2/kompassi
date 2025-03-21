import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";

import { graphql } from "@/__generated__";
import { ProgramOfferFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import { Dimension } from "@/components/dimensions/models";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import UploadedFileLink from "@/components/forms/UploadedFileLink";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment ProgramOffer on FullResponseType {
    id
    createdAt
    createdBy {
      displayName
    }
    sequenceNumber
    values(keyFieldsOnly: true)
    form {
      survey {
        title(lang: $locale)
      }
      language
    }
  }
`);

const query = graphql(`
  query ProgramOffers($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      slug
      name
      program {
        countProgramOffers
        programOffers {
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

export default async function FormResponsesPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.ProgramOffer;
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

  const dimensions: Dimension[] = []; // TODO
  const keyFields: Field[] = [
    {
      slug: "title",
      type: "SingleLineText",
      title: programT.attributes.title,
    },
  ];

  const columns: Column<ProgramOfferFragment>[] = [
    {
      slug: "sequenceNumber",
      title: "#",
    },
    {
      slug: "createdAt",
      title: surveyT.attributes.createdAt,
      getCellContents: (row) => (
        <Link href={`/${eventSlug}/program-offers/${row.id}`}>
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
      getCellContents: (row) => row.createdBy?.displayName || "",
    },
    {
      slug: "form",
      title: programT.ProgramForm.singleTitle,
      getCellContents: (row) =>
        `${row.form.survey?.title || ""} (${row.form.language})`,
    },
  ];

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

  // TODO Key dimensions
  // columns.push(...buildKeyDimensionColumns(dimensions));

  const programOffers = data.event.program.programOffers || [];

  // TODO ProgramAdminView
  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programOffers"
    >
      <DimensionFilters dimensions={dimensions} />
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
