import Link from "next/link";
import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardTitle from "react-bootstrap/CardTitle";
import { markAsFavorite, unmarkAsFavorite } from "./actions";
import FavoriteButton from "./FavoriteButton";
import { FavoriteContextProvider } from "./FavoriteContext";
import { graphql } from "@/__generated__";
import { ProgramListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { decodeBoolean } from "@/helpers/decodeBoolean";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramList on ProgramType {
    slug
    title
    cachedDimensions
    color
    scheduleItems {
      startTime
      endTime
      location
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

          values {
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
  const t = getTranslations(locale).Program;
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

  const favoritesOnly = !!searchParams.favorited;
  const userPrograms = data.profile?.program?.programs || [];
  const programs = favoritesOnly ? userPrograms : event.program.programs;
  const listFilters = event.program.listFilters || [];
  const favoriteProgramSlugs = userPrograms.map((p) => p.slug);

  const queryString = new URLSearchParams(searchParams).toString();
  const calendarExportLink = queryString
    ? `${event.program.calendarExportLink}?${queryString}`
    : event.program.calendarExportLink;

  function getCardStyle(program: ProgramListFragment) {
    return program.color ? { borderLeft: `4px solid ${program.color}` } : {};
  }

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
        slugs={favoriteProgramSlugs}
        messages={t.favorites}
        markAsFavorite={markAsFavorite.bind(null, locale, eventSlug)}
        unmarkAsFavorite={unmarkAsFavorite.bind(null, locale, eventSlug)}
      >
        {programs.map((program) => (
          <Card
            key={program.slug}
            className="mb-3"
            style={getCardStyle(program)}
          >
            <CardBody>
              <div className="d-flex justify-content-between">
                <CardTitle>
                  <CardLink
                    as={Link}
                    href={`/events/${eventSlug}/programs/${program.slug}`}
                    className="link-subtle"
                  >
                    {program.title}
                  </CardLink>
                </CardTitle>
                {data.profile && <FavoriteButton slug={program.slug} />}
              </div>
              {program.scheduleItems.map((scheduleItem, index) => (
                <div key={index} className="d-flex justify-content-between">
                  <div>
                    <FormattedDateTimeRange
                      locale={locale}
                      scope={event}
                      session={null}
                      start={scheduleItem.startTime}
                      end={scheduleItem.endTime}
                      includeDuration={true}
                    />
                  </div>
                  <div>{scheduleItem.location}</div>
                </div>
              ))}
            </CardBody>
          </Card>
        ))}
      </FavoriteContextProvider>

      <p className="mt-4">
        <a href={calendarExportLink} className="link-subtle">
          📅 {t.actions.addTheseToCalendar}…
        </a>
      </p>
    </ViewContainer>
  );
}
