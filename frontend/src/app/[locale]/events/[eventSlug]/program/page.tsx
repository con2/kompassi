import Link from "next/link";
import { notFound } from "next/navigation";

import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardLink from "react-bootstrap/CardLink";
import CardText from "react-bootstrap/CardText";
import CardTitle from "react-bootstrap/CardTitle";
import { markAsFavorite } from "./actions";
import classes from "./page.module.css";
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
              {/* TODO(#469)
              <form
                action={markAsFavorite.bind(null, {
                  eventSlug,
                  programSlug: program.slug,
                })}
                className={classes.favoriteForm}
              >
                <Button
                  type="submit"
                  variant="link"
                  className={classes.favorite}
                  title="Mark as favorite"
                >
                  ⭐
                </Button>
              </form> */}
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
    </ViewContainer>
  );
}
