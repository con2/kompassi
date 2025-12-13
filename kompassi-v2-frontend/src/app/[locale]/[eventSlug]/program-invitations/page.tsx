import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProgramAdminInvitationFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramAdminInvitation on FullInvitationType {
    id
    email
    createdAt
    cachedDimensions

    program {
      slug
      title
    }
  }
`);

const query = graphql(`
  query ProgramAdminInvitations($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        invitations {
          ...ProgramAdminInvitation
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
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

export default async function ProgramAdminInvitationsPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const profileT = translations.Profile;
  const t = translations.Invitation;
  const programT = translations.Program;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  if (!data.event?.program?.invitations) {
    notFound();
  }

  const event = data.event;
  const invitations = data.event.program.invitations;

  const columns: Column<ProgramAdminInvitationFragment>[] = [
    {
      slug: "program",
      title: programT.singleTitle,
      getCellContents: (row) => (
        <Link
          href={`/${event.slug}/program-admin/${row.program?.slug}/hosts`}
          className="link-subtle"
        >
          {row.program?.title}
        </Link>
      ),
    },
    {
      slug: "email",
      title: profileT.advancedAttributes.email.title,
      getCellContents: (row) => row.email,
    },
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (row) => (
        <FormattedDateTime
          value={row.createdAt}
          locale={locale}
          scope={event}
          session={session}
        />
      ),
    },
  ];

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active={"invitations"}
      searchParams={searchParams}
    >
      <DataTable rows={invitations} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.attributes.count(invitations.length)}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminView>
  );
}
