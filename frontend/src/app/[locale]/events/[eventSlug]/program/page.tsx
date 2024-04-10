import Link from "next/link";
import { notFound } from "next/navigation";

import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardText from "react-bootstrap/CardText";
import CardTitle from "react-bootstrap/CardTitle";
import { markAsFavorite, unmarkAsFavorite } from "./actions";
import FavoriteButton from "./FavoriteButton";
import { FavoriteContextProvider } from "./FavoriteContext";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import {
  buildDimensionFilters,
  getDimensionValueTitle,
} from "@/components/dimensions/helpers";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramList on ProgramType {
    slug
    title
    cachedDimensions
    scheduleItems {
      startTime
      endTime
    }
  }
`);

const query = graphql(`
  query ProgramListQuery(
    $eventSlug: String!
    $locale: String
    $filters: [DimensionFilterInput!]
  ) {
    profile {
      program {
        programs(eventSlug: $eventSlug, filters: $filters) {
          slug
        }
      }
    }

    event(slug: $eventSlug) {
      name
      slug

      program {
        calendarExportLink

        dimensions {
          slug
          title(lang: $locale)

          values {
            slug
            title(lang: $locale)
          }
        }

        programs(filters: $filters) {
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
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
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

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });
  const { event } = data;

  if (!event?.program?.programs) {
    notFound();
  }

  const programs = event.program.programs;
  const dimensions = event.program.dimensions || [];
  const roomDimension = dimensions.find((d) => d.slug === "room");

  const userPrograms = data.profile?.program?.programs || [];
  const favoriteProgramSlugs = userPrograms.map((p) => p.slug);

  const queryString = new URLSearchParams(searchParams).toString();
  const calendarExportLink = queryString
    ? `${event.program.calendarExportLink}?${queryString}`
    : event.program.calendarExportLink;

  return (
    <ViewContainer>
      <ViewHeading>
        {t.listTitle}
        <ViewHeading.Sub>{t.inEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <DimensionFilters dimensions={dimensions}></DimensionFilters>
      <FavoriteContextProvider
        slugs={favoriteProgramSlugs}
        messages={t.favorites}
        markAsFavorite={markAsFavorite.bind(null, locale, eventSlug)}
        unmarkAsFavorite={unmarkAsFavorite.bind(null, locale, eventSlug)}
      >
        {programs.map((program) => (
          <Card key={program.slug} className="mb-4">
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
              <div className="d-flex justify-content-between">
                <div>
                  {program.scheduleItems.map((scheduleItem, index) => (
                    <CardText key={index}>
                      <FormattedDateTimeRange
                        locale={locale}
                        scope={event}
                        session={null}
                        start={scheduleItem.startTime}
                        end={scheduleItem.endTime}
                        includeDuration={true}
                      />
                    </CardText>
                  ))}
                </div>
                <CardText>
                  {roomDimension &&
                    getDimensionValueTitle(
                      roomDimension,
                      program.cachedDimensions,
                    )}
                </CardText>
              </div>
            </CardBody>
          </Card>
        ))}
      </FavoriteContextProvider>

      <p className="mt-4">
        <a href={calendarExportLink} className="link-subtle">
          {t.actions.addTheseToCalendar}…
        </a>
      </p>
    </ViewContainer>
  );
}
