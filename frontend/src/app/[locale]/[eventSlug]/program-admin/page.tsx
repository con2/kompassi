import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";

import { graphql } from "@/__generated__";
import {
  ProgramAdminFragment,
  ProgramOfferFragment,
} from "@/__generated__/graphql";
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
  fragment ProgramAdmin on FullProgramType {
    slug
    title
  }
`);

const query = graphql(`
  query ProgramAdminList($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      slug
      name
      program {
        listFilters: dimensions(isListFilter: true) {
          slug
          title(lang: $locale)
          isListFilter

          values(lang: $locale) {
            slug
            title(lang: $locale)
            color
          }
        }

        programs {
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

  const columns: Column<ProgramAdminFragment>[] = [
    {
      slug: "title",
      title: t.attributes.title,
    },
  ];

  const listFilters = data.event?.program.listFilters;
  const programs = data.event?.program?.programs;

  // TODO Key dimensions
  // columns.push(...buildKeyDimensionColumns(dimensions));

  // TODO ProgramAdminView
  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programItems"
    >
      <DimensionFilters dimensions={listFilters} />
      <DataTable rows={programs} columns={columns}></DataTable>
    </ProgramAdminView>
  );
}
