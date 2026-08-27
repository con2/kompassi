import { ViewContainer, ViewHeading } from "@con2/components";
import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import getPageTitle from "@/helpers/getPageTitle";
import ProgramDetail from "@/components/program/ProgramDetail";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramDetailQuery(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    profile {
      program {
        scheduleItems(eventSlug: $eventSlug) {
          slug
        }
      }
    }

    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        program(slug: $programSlug) {
          ...ProgramDetail
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
}

export const revalidate = 5;

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
    viewTitle: translations.Program.singleTitle,
    subject: data?.event?.program?.program?.title,
  });
  const description = data?.event?.program?.program?.description;
  return { title, description };
}

export default async function NewProgramPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const { event } = data;
  if (!event?.program?.program) {
    notFound();
  }

  const program = event.program.program;
  const favoriteScheduleItemSlugs =
    data.profile?.program?.scheduleItems?.map(
      (scheduleItem) => scheduleItem.slug,
    ) ?? [];

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${eventSlug}/program`}>
        &lt; {t.actions.returnToProgramList(event.name)}
      </Link>

      <ViewHeading>{program.title}</ViewHeading>

      <ProgramDetail
        locale={locale}
        event={event}
        program={program}
        isLoggedIn={!!data.profile}
        favoriteScheduleItemSlugs={favoriteScheduleItemSlugs}
        listUrl={`/${eventSlug}/program`}
        translations={translations}
      />
    </ViewContainer>
  );
}
