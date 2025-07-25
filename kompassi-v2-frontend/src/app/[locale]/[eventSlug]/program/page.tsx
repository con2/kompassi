import { notFound } from "next/navigation";

import { markScheduleItemAsFavorite, unmarkAsFavorite } from "./actions";
import { FavoriteContextProvider } from "./FavoriteContext";
import ProgramCard from "./ProgramCard";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { decodeBoolean } from "@/helpers/decodeBoolean";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ScheduleProgram on LimitedProgramType {
    slug
    title
    cachedDimensions
    color
    isCancelled
  }
`);

graphql(`
  fragment ScheduleItemList on FullScheduleItemType {
    slug
    location(lang: $locale)
    subtitle
    startTime
    endTime
    program {
      ...ScheduleProgram
    }
  }
`);

const query = graphql(`
  query ProgramListQuery(
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

        listFilters: dimensions(isListFilter: true) {
          ...DimensionFilter
        }

        scheduleItems(filters: $filters, hidePast: $hidePast) {
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

// TODO move favorites into a client component
export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const filters = buildDimensionFilters(searchParams);
  const hidePast = !!searchParams.past && !decodeBoolean(searchParams.past);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters, hidePast },
  });
  const { event } = data;
  const translations = getTranslations(locale);
  const title = getPageTitle({
    translations,
    event,
    viewTitle: translations.Program.listTitle,
    subject: null,
  });
  return {
    title,
  };
}

export default async function ProgramListPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
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

  const session = await auth();
  const favoritesOnly = session && !!searchParams.favorited;
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

  return (
    <ViewContainer>
      <ViewHeading>
        {t.listTitle}
        <ViewHeading.Sub>{t.inEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <DimensionFilters
        dimensions={listFilters}
        programFilters={true}
        messages={t.filters}
        isLoggedIn={!!data.profile}
      />
      <FavoriteContextProvider
        slugs={favoriteScheduleItemSlugs}
        messages={t.favorites}
        markAsFavorite={markScheduleItemAsFavorite.bind(
          null,
          locale,
          eventSlug,
        )}
        unmarkAsFavorite={unmarkAsFavorite.bind(null, locale, eventSlug)}
      >
        <div className="mt-3">
          {scheduleItems.map((scheduleItem) => (
            <ProgramCard
              key={scheduleItem.slug}
              program={scheduleItem.program}
              scheduleItem={scheduleItem}
              event={event}
              isLoggedIn={!!data.profile}
              locale={locale}
              messages={t}
            />
          ))}
        </div>
        {/* )} */}
      </FavoriteContextProvider>

      <p className="mt-4">
        <a href={calendarExportLink} className="link-subtle">
          📅 {t.actions.addTheseToCalendar}…
        </a>
      </p>
    </ViewContainer>
  );
}
