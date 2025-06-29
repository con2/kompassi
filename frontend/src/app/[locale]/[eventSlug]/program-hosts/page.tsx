// TODO Filter program hosts by dimensions
// Should these be program dimensions or involvement dimensions? Probably program.

import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProgramAdminHostFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramAdminHost on FullProgramHostType {
    person {
      firstName
      lastName
      nick
    }
    programs {
      slug
      title
      cachedDimensions
    }
  }
`);

const query = graphql(`
  query ProgramAdminHosts(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        dimensions(isListFilter: true, publicOnly: false) {
          ...DimensionFilter
        }
        programHosts(programFilters: $filters) {
          ...ProgramAdminHost
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

export const revalidate = 0;

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const filters = buildDimensionFilters(searchParams);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.ProgramHost.listTitle,
  });
  return { title };
}

export default async function ProgramAdminHostsPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const profileT = translations.Profile;
  const t = translations.Program.ProgramHost;
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
  if (!data.event?.program?.programHosts) {
    notFound();
  }

  const event = data.event;
  const programHosts = data.event.program.programHosts;

  // TODO ugly. showing active only
  const dimensions = data.event.program.dimensions.filter(
    (dimension) => dimension.slug !== "state",
  );

  const columns: Column<ProgramAdminHostFragment>[] = [
    {
      slug: "lastName",
      title: profileT.advancedAttributes.lastName.title,
      getCellContents: (row) => row.person.lastName,
    },
    {
      slug: "firstName",
      title: profileT.advancedAttributes.firstName.title,
      getCellContents: (row) => row.person.firstName,
    },
    {
      slug: "nick",
      title: profileT.advancedAttributes.nick.title,
      getCellContents: (row) => row.person.nick,
    },
    {
      slug: "programItems",
      title: t.attributes.programItems,
      getCellContents: (row) => (
        <>
          {row.programs.map((program) => (
            <div key={program.slug}>
              <Link
                href={`/${event.slug}/program-admin/${program.slug}`}
                className="link-subtle"
              >
                {program.title}
              </Link>
            </div>
          ))}
        </>
      ),
    },
  ];

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active={"programHosts"}
      searchParams={searchParams}
    >
      <DimensionFilters
        dimensions={dimensions}
        className="row row-cols-md-auto g-3 align-items-center mb-4 mt-1"
      />
      <DataTable rows={programHosts} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.attributes.count(programHosts.length)}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminView>
  );
}
