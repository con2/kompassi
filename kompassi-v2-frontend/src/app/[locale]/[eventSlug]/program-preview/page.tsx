import { SignInRequired } from "@con2/components";
import { decodeBoolean } from "@con2/components/helpers";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import ProgramList from "@/components/program/ProgramList";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Alert } from "react-bootstrap";

const query = graphql(`
  query ProgramPreviewListQuery(
    $locale: String
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $hidePast: Boolean
  ) {
    profile {
      program {
        scheduleItems(
          eventSlug: $eventSlug
          filters: $filters
          hidePast: $hidePast
        ) {
          ...ScheduleItemList
        }
      }
    }

    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        calendarExportLink
        isSchedulePublic

        listFilters: dimensions(isListFilter: true) {
          ...DimensionFilter
        }

        scheduleItems(
          filters: $filters
          hidePast: $hidePast
          publicOnly: false
        ) {
          ...ScheduleItemList
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
  const params = await props.params;
  const { locale } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const searchParams = await props.searchParams;
  const { eventSlug } = params;
  const filters = buildDimensionFilters(searchParams);
  const hidePast = !!searchParams.past && !decodeBoolean(searchParams.past);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters, hidePast },
  });
  const { event } = data;
  const title = getPageTitle({
    translations,
    event,
    viewTitle: translations.Program.actions.preview,
    subject: null,
  });
  return {
    title,
  };
}

export default async function ProgramPreviewListPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;

  const session = await auth();

  // TODO encap
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const filters = buildDimensionFilters(searchParams);
  const hidePast = !!searchParams.past && !decodeBoolean(searchParams.past);

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters, hidePast },
  });
  const { event } = data;

  if (!event?.program?.scheduleItems) {
    notFound();
  }

  const favoritesOnly = !!searchParams.favorited;
  const userScheduleItems = data.profile?.program?.scheduleItems || [];
  const scheduleItems = favoritesOnly
    ? userScheduleItems
    : event.program.scheduleItems;
  const listFilters = event.program.listFilters || [];
  const favoriteScheduleItemSlugs = userScheduleItems.map((p) => p.slug);

  const urlSearchParams = new URLSearchParams(searchParams);
  const queryString = urlSearchParams.toString();
  const calendarExportLink = queryString
    ? `${event.program.calendarExportLink}?${queryString}`
    : event.program.calendarExportLink;

  const alerts = !event.program.isSchedulePublic && (
    <Alert variant="warning">{t.scheduleNotPublic}</Alert>
  );

  return (
    <ProgramAdminView
      translations={translations}
      event={event}
      active="preview"
      searchParams={searchParams}
      alerts={alerts}
    >
      <div className="mt-3">
        <ProgramList
          locale={locale}
          event={event}
          scheduleItems={scheduleItems}
          listFilters={listFilters}
          favoriteScheduleItemSlugs={favoriteScheduleItemSlugs}
          isLoggedIn={!!data.profile}
          calendarExportLink={calendarExportLink}
          programBaseUrl={`/${eventSlug}/program-preview`}
          messages={t}
        />
      </div>
    </ProgramAdminView>
  );
}
