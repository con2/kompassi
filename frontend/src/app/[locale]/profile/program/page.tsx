import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import {
  ProfileProgramItemFragment,
  ProfileResponsesTableRowFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import FormattedDateTimeRange, {
  formatDurationMinutes,
} from "@/components/FormattedDateTimeRange";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileProgramItem on FullProgramType {
    slug
    title
    event {
      slug
      name
      timezone
    }
    scheduleItems {
      slug
      startTime
      endTime
      durationMinutes
      location(lang: $locale)
      subtitle
    }
  }
`);

const query = graphql(`
  query ProfileProgramItemList($locale: String!) {
    profile {
      program {
        programs(userRelation: HOSTING) {
          ...ProfileProgramItem
        }

        programOffers(filters: [{ dimension: "state", values: "new" }]) {
          ...ProfileResponsesTableRow
        }
      }
    }
  }
`);

function ProgramLink({
  program,
  children,
}: {
  program: ProfileProgramItemFragment;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={`/${program.event.slug}/programs/${program.slug}`}
      className="link-subtle"
    >
      {children}
    </Link>
  );
}

function ProgramOfferLink({
  programOffer,
  children,
}: {
  programOffer: ProfileResponsesTableRowFragment;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={`/profile/responses/${programOffer.id}`}
      className="link-subtle"
    >
      {children}
    </Link>
  );
}

interface Props {
  params: {
    locale: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;

  const title = getPageTitle({
    viewTitle: t.profile.title,
    translations,
  });

  return { title };
}

export const revalidate = 0;

export default async function ProfileProgramItemList({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const surveyT = translations.Survey;
  const scheduleT = translations.Program.ScheduleItem;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: {
      locale,
    },
  });

  if (!data.profile?.program.programs) {
    notFound();
  }

  const programItemColumns: Column<ProfileProgramItemFragment>[] = [
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.event.name,
    },
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents: (row) => (
        <ProgramLink program={row}>{row.title}</ProgramLink>
      ),
    },
    {
      slug: "time",
      title: scheduleT.attributes.time.title,
      getCellContents: (row) =>
        row.scheduleItems.map((scheduleItem) => (
          <div key={scheduleItem.slug}>
            {scheduleItem.subtitle && (
              <>
                <em>{scheduleItem.subtitle}:</em>{" "}
              </>
            )}
            <FormattedDateTimeRange
              start={scheduleItem.startTime}
              end={scheduleItem.endTime}
              locale={locale}
              session={session}
              scope={row.event}
            />{" "}
            ({formatDurationMinutes(scheduleItem.durationMinutes, locale)})
          </div>
        )),
    },
    {
      slug: "location",
      title: scheduleT.attributes.location.title,
      getCellContents: (row) =>
        row.scheduleItems.map((scheduleItem) => (
          <div key={scheduleItem.slug}>{scheduleItem.location}</div>
        )),
    },
    {
      slug: "actions",
      title: "",
      className: "text-end align-middle",
      getCellContents: (program) => {
        return (
          <ProgramLink program={program}>
            🔍 {surveyT.actions.viewResponse.label}
          </ProgramLink>
        );
      },
    },
  ];

  const programOfferColumns: Column<ProfileResponsesTableRowFragment>[] = [
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (row) => row.form.event.name,
    },
    {
      slug: "title",
      title: t.attributes.title,
      getCellContents: (row) => (
        <ProgramOfferLink programOffer={row}>
          {(row.values as Record<string, any>).title ?? ""}
        </ProgramOfferLink>
      ),
    },
    {
      slug: "revisionCreatedAt",
      title: surveyT.attributes.currentVersionCreatedAt,
      getCellContents: (row) => (
        <FormattedDateTime
          value={row.revisionCreatedAt}
          locale={locale}
          scope={row.form.event}
          session={session}
        />
      ),
    },
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => {
        return (
          <>
            {row.canEdit && (
              <Link
                href={`/profile/responses/${row.id}/edit`}
                className="link-subtle me-3"
              >
                ✏ {surveyT.actions.editResponse.label}
              </Link>
            )}
            <ProgramOfferLink programOffer={row}>
              🔍 {surveyT.actions.viewResponse.label}
            </ProgramOfferLink>
          </>
        );
      },
    },
  ];

  const programItems = data.profile.program.programs;
  const programOffers = data.profile.program.programOffers;

  return (
    <ViewContainer>
      <ViewHeading>{t.profile.title}</ViewHeading>
      {programItems.length > 0 && (
        <>
          <p>{t.profile.programItems.listTitle}:</p>
          <DataTable rows={programItems} columns={programItemColumns}>
            <tfoot>
              <tr>
                <td colSpan={programItemColumns.length}>
                  {t.profile.programItems.tableFooter(programItems.length)}
                </td>
              </tr>
            </tfoot>
          </DataTable>
        </>
      )}
      {programOffers.length > 0 && (
        <>
          <p>{t.profile.programOffers.listTitle}:</p>
          <DataTable columns={programOfferColumns} rows={programOffers} />
        </>
      )}
      {programItems.length === 0 && programOffers.length === 0 && (
        <p>{t.profile.empty}</p>
      )}
      <p className="mt-4">
        {t.profile.allProgramOffers}{" "}
        <Link href="/profile/responses" className="link-subtle">
          {translations.Survey.ownResponsesTitle}
        </Link>
      </p>
    </ViewContainer>
  );
}
