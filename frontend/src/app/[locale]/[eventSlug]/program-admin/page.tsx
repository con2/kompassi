import Link from "next/link";
import { notFound } from "next/navigation";

import { createProgram } from "./actions";
import { graphql } from "@/__generated__";
import { ProgramAdminFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { buildKeyDimensionColumns } from "@/components/dimensions/ColoredDimensionTableCell";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionValueSelectionForm } from "@/components/dimensions/DimensionValueSelectionForm";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import Messages from "@/components/errors/Messages";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
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
        dimensions(publicOnly: false) {
          slug
          title(lang: $locale)
          isTechnical
          isMultiValue
          isKeyDimension
          isListFilter

          values(lang: $locale) {
            slug
            title(lang: $locale)
            color
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
  const surveyT = translations.Survey;
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

  const dimensions = data.event.program.dimensions;
  const listFilters = dimensions.filter((dimension) => dimension.isListFilter);
  const programs = data.event.program.programs;
  const event = data.event;
  const keyDimensions = dimensions.filter(
    (dimension) => dimension.isKeyDimension,
  );

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
  ];

  columns.push(...buildKeyDimensionColumns(keyDimensions));

  // Create program item form

  const { fields: dimensionFields } = buildDimensionValueSelectionForm(
    dimensions,
    {},
  );

  const createProgramFields: Field[] = [
    {
      slug: "slug",
      required: true,
      type: "SingleLineText",
      ...t.attributes.slug,
    },
    {
      slug: "title",
      title: t.attributes.title,
      required: true,
      type: "SingleLineText",
    },
    {
      slug: "description",
      title: t.attributes.description,
      type: "MultiLineText",
      rows: 5,
    },
  ];
  if (dimensions.filter((dimension) => !dimension.isTechnical).length > 0) {
    createProgramFields.push(
      {
        slug: "dimensionsHeader",
        type: "StaticText",
        title: surveyT.attributes.dimensions,
      },
      ...dimensionFields,
    );
  }

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programItems"
      searchParams={searchParams}
      actions={
        <ModalButton
          className="btn btn-outline-primary"
          label={t.actions.create.title + "…"}
          title={t.actions.create.title}
          messages={t.actions.create.modalActions}
          action={createProgram.bind(null, locale, eventSlug)}
        >
          <SchemaForm
            fields={createProgramFields}
            messages={translations.SchemaForm}
            headingLevel="h4"
          />
        </ModalButton>
      }
    >
      <DimensionFilters
        dimensions={listFilters}
        className="row row-cols-md-auto g-3 align-items-center mb-4 mt-1 xxx-this-is-horrible"
      />
      <DataTable rows={programs} columns={columns}></DataTable>
    </ProgramAdminView>
  );
}
