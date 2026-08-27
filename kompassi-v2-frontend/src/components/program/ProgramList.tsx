import { markScheduleItemAsFavorite, unmarkAsFavorite } from "./actions";
import { FavoriteContextProvider } from "./FavoriteContext";
import ProgramCard from "./ProgramCard";
import { Scope } from "./models";
import { graphql } from "@/__generated__";
import {
  DimensionFilterFragment,
  ScheduleItemListFragment,
} from "@/__generated__/graphql";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import type { Translations } from "@/translations/en";

graphql(`
  fragment ScheduleProgram on LimitedProgramType {
    slug
    title
    cachedDimensions(publicOnly: true, listFiltersOnly: true)
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

interface Props {
  locale: string;
  event: Scope;
  scheduleItems: ScheduleItemListFragment[];
  listFilters: DimensionFilterFragment[];
  favoriteScheduleItemSlugs: string[];
  isLoggedIn: boolean;
  calendarExportLink: string;
  /// `/${eventSlug}/programs` on the public list, `/${eventSlug}/program-preview` on the preview.
  programBaseUrl: string;
  messages: Translations["Program"];
}

export default function ProgramList({
  locale,
  event,
  scheduleItems,
  listFilters,
  favoriteScheduleItemSlugs,
  isLoggedIn,
  calendarExportLink,
  programBaseUrl,
  messages: t,
}: Props) {
  return (
    <>
      <DimensionFilters
        dimensions={listFilters}
        programFilters={true}
        messages={t.filters}
        isLoggedIn={isLoggedIn}
      />
      <FavoriteContextProvider
        /* Force favorite buttons to re-render with refreshed data when filters change */
        key={JSON.stringify(favoriteScheduleItemSlugs)}
        slugs={favoriteScheduleItemSlugs}
        messages={t.favorites}
        markAsFavorite={markScheduleItemAsFavorite.bind(
          null,
          locale,
          event.slug,
        )}
        unmarkAsFavorite={unmarkAsFavorite.bind(null, locale, event.slug)}
      >
        <div className="mt-3">
          {scheduleItems.map((scheduleItem) => (
            <ProgramCard
              key={scheduleItem.slug}
              program={scheduleItem.program}
              scheduleItem={scheduleItem}
              event={event}
              isLoggedIn={isLoggedIn}
              locale={locale}
              href={`${programBaseUrl}/${scheduleItem.program.slug}`}
              messages={t}
            />
          ))}
        </div>
      </FavoriteContextProvider>

      <p className="mt-4">
        <a href={calendarExportLink} className="link-subtle">
          📅 {t.actions.addTheseToCalendar}…
        </a>
      </p>
    </>
  );
}
