import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import {
  ProgramAdminDetailHostFragment,
  ProgramAdminHostFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { Column, DataTable } from "@/components/DataTable";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
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
  query ProgramAdminHosts($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        programHosts {
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
  queryParams: Record<string, string>;
}

export const revalidate = 0;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.ProgramHost.listTitle,
  });
  return { title };
}

export default async function ProgramAdminDetailPage({
  params,
  queryParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const profileT = translations.Profile;
  const t = translations.Program.ProgramHost;
  const queryString = new URLSearchParams(queryParams).toString();

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  if (!data.event?.program?.programHosts) {
    notFound();
  }

  const event = data.event;
  const programHosts = data.event.program.programHosts;

  const columns: Column<ProgramAdminHostFragment>[] = [
    {
      slug: "lastName",
      title: profileT.attributes.lastName.title,
      getCellContents: (row) => row.person.lastName,
    },
    {
      slug: "firstName",
      title: profileT.attributes.firstName.title,
      getCellContents: (row) => row.person.firstName,
    },
    {
      slug: "nick",
      title: profileT.attributes.nick.title,
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
      queryString={queryString}
    >
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
