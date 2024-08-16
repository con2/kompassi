import { notFound } from "next/navigation";

import { markAsFavorite, unmarkAsFavorite } from "./actions";
import { FavoriteContextProvider } from "./FavoriteContext";
import ProgramCard from "./ProgramCard";
import ProgramTable from "./ProgramTable";
import ProgramTabs from "./ProgramTabs";
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
  fragment ScheduleItem on ScheduleItemType {
    location
    subtitle
    startTime
    endTime
  }
`);

graphql(`
  fragment ProgramList on ProgramType {
    slug
    title
    cachedDimensions
    color
    scheduleItems {
      ...ScheduleItem
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
        programs(
          eventSlug: $eventSlug
          filters: $filters
          hidePast: $hidePast
        ) {
          ...ProgramList
        }
      }
    }

    event(slug: $eventSlug) {
      name
      slug

      program {
        calendarExportLink

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

        programs(filters: $filters, hidePast: $hidePast) {
          ...ProgramList
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

// TODO move favorites into a client component
export const revalidate = 0;

export async function generateMetadata({ params, searchParams }: Props) {
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

export default async function ProgramListPage({ params, searchParams }: Props) {
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

  if (!event?.program?.programs) {
    notFound();
  }

  const session = await auth();
  const favoritesOnly = session && !!searchParams.favorited;
  const userPrograms = data.profile?.program?.programs || [];
  const programs = favoritesOnly ? userPrograms : event.program.programs;
  const listFilters = event.program.listFilters || [];
  const favoriteProgramSlugs = userPrograms.map((p) => p.slug);

  const urlSearchParams = new URLSearchParams(searchParams);
  const activeTab =
    urlSearchParams.get("display") === "table" ? "table" : "cards";
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
      <ProgramTabs
        searchParams={searchParams}
        eventSlug={event.slug}
        active={activeTab}
        translations={translations}
      />
      <FavoriteContextProvider
        slugs={favoriteProgramSlugs}
        messages={t.favorites}
        markAsFavorite={markAsFavorite.bind(null, locale, eventSlug)}
        unmarkAsFavorite={unmarkAsFavorite.bind(null, locale, eventSlug)}
      >
        {activeTab === "table" ? (
          <ProgramTable
            programs={programs}
            event={event}
            locale={locale}
            isLoggedIn={!!data.profile}
            translations={translations}
          />
        ) : (
          <div className="mt-3">
            {programs.map((program) => (
              <ProgramCard
                key={event.slug}
                program={program}
                event={event}
                isLoggedIn={!!data.profile}
                locale={locale}
              />
            ))}
          </div>
        )}
      </FavoriteContextProvider>

      <p className="mt-4">
        <a href={calendarExportLink} className="link-subtle">
          📅 {t.actions.addTheseToCalendar}…
        </a>
      </p>
    </ViewContainer>
  );
}
