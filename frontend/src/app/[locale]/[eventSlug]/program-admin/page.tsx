import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProgramAdminFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment ProgramAdmin on FullProgramType {
    slug
    title
    scheduleItems {
      startTime
    }
    cachedDimensions
  }
`);

const query = graphql(`
  query ProgramAdminList(
    $eventSlug: String!
    $locale: String
    $filters: [DimensionFilterInput!]
  ) {
    event(slug: $eventSlug) {
      slug
      name
      program {
        listFilters: dimensions(isListFilter: true, publicOnly: false) {
          slug
          title(lang: $locale)

          values(lang: $locale) {
            slug
            title(lang: $locale)
            color
          }
        }

        keyDimensions: dimensions(keyDimensionsOnly: true, publicOnly: false) {
          slug
          title(lang: $locale)

          values(lang: $locale) {
            slug
            title(lang: $locale)
          }
        }

        programs(filters: $filters) {
          ...ProgramAdmin
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

  const t = translations.Program;

  // while dimension filters are not needed to form the title,
  // we would like to do only one query per request
  // so do the exact same query here so that it can be cached
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });

  if (!data.event?.program?.programs) {
    notFound();
  }

  const title = getPageTitle({
    viewTitle: t.adminListTitle,
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
  const t = translations.Program;
  const scheduleT = translations.Program.ScheduleItem;
  const queryString = new URLSearchParams(searchParams).toString();

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

  if (!data.event?.program?.programs) {
    notFound();
  }

  const listFilters = data.event.program.listFilters;
  const programs = data.event.program.programs;
  const event = data.event;
  const keyDimensions = data.event.program.keyDimensions;

  const columns: Column<ProgramAdminFragment>[] = [
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents: (program) => (
        <Link
          href={`/${event.slug}/program-admin/${program.slug}?${queryString}`}
        >
          {program.title}
        </Link>
      ),
    },
    {
      slug: "startTime",
      title: scheduleT.attributes.startTime,
    },
  ];

  columns.push(...buildKeyDimensionColumns(keyDimensions));

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programItems"
      queryString={queryString}
    >
      <DimensionFilters
        dimensions={listFilters}
        className="row row-cols-md-auto g-3 align-items-center mb-4 mt-1 xxx-this-is-horrible"
      />
      <DataTable rows={programs} columns={columns}></DataTable>
    </ProgramAdminView>
  );
}
