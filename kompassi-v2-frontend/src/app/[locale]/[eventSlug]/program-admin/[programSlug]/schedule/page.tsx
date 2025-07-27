import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import ScheduleItemTable from "./ScheduleItemsTable";

graphql(`
  fragment ProgramAdminDetailScheduleItem on LimitedScheduleItemType {
    slug
    title
    subtitle
    location(lang: $locale)
    startTime
    durationMinutes
    room
    freeformLocation
  }
`);

const query = graphql(`
  query ProgramAdminDetailSchedule(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        dimensions {
          ...DimensionValueSelect
        }

        program(slug: $programSlug) {
          slug
          title

          dimensions(publicOnly: false) {
            ...ProgramDimensionBadge
          }

          scheduleItems {
            ...ProgramAdminDetailScheduleItem
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    programSlug: string;
  }>;
  searchParams: Promise<{
    success?: string;
  }>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.attributes.scheduleItems.title,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramAdminDetailSchedulePage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;
  const scheduleItems = program.scheduleItems;
  const dimensions = data.event.program.dimensions;

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"scheduleItems"}
      searchParams={searchParams}
    >
      <ScheduleItemTable
        locale={locale}
        event={event}
        program={program}
        dimensions={dimensions}
        scheduleItems={scheduleItems}
      />
    </ProgramAdminDetailView>
  );
}
