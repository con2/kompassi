import { SignInRequired } from "@con2/components";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import ProgramDetail from "@/components/program/ProgramDetail";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramPreviewDetailQuery(
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
          adminDimensions: dimensions(publicOnly: false) {
            ...ProgramDimensionBadge
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
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });

  if (!data.event?.program?.program) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.adminDetailTabs.preview,
    subject: data.event.program.program.title,
  });

  return { title };
}

export default async function ProgramPreviewDetailPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
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
    <ProgramAdminDetailView
      event={event}
      program={{
        slug: program.slug,
        title: program.title,
        dimensions: program.adminDimensions,
      }}
      translations={translations}
      active="preview"
      searchParams={searchParams}
    >
      <div className="mt-4">
        <ProgramDetail
          locale={locale}
          event={event}
          program={program}
          isLoggedIn={!!data.profile}
          favoriteScheduleItemSlugs={favoriteScheduleItemSlugs}
          listUrl={`/${eventSlug}/program-preview`}
          translations={translations}
        />
      </div>
    </ProgramAdminDetailView>
  );
}
