import Link from "next/link";
import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardText from "react-bootstrap/CardText";
import CardTitle from "react-bootstrap/CardTitle";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
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
    event(slug: $eventSlug) {
      name
      slug

      program {
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

export const revalidate = 5;

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, filters },
  });
  const { event } = data;
  const translations = getTranslations(locale);
  return getPageTitle({
    translations,
    event,
    viewTitle: translations.Program.listTitle,
    subject: null,
  });
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

  return (
    <ViewContainer>
      <ViewHeading>
        {t.listTitle}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <DimensionFilters dimensions={dimensions}></DimensionFilters>
      {programs.map((program) => (
        <Card key={program.slug} className="mb-4">
          <CardBody>
            <CardTitle>
              <CardLink
                as={Link}
                href={`/events/${eventSlug}/programs/${program.slug}`}
              >
                {program.title}
              </CardLink>
            </CardTitle>
            {/* TODO FormattedDateTimeRange */}
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
    </ViewContainer>
  );
}
