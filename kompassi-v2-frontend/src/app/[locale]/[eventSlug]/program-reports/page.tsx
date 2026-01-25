import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import Report from "@/components/reports/Report";
import { timezone as defaultTimezone } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramAdminReportsPage($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        reports(lang: $locale) {
          ...Report
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
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug },
  });

  if (!data.event?.program) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: translations.Report.listTitle,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ProgramReportsPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug },
  });

  if (!data.event?.program) {
    notFound();
  }

  const event = data.event;
  const timezone = event.timezone || defaultTimezone;
  const { reports } = data.event.program;

  return (
    <ProgramAdminView
      translations={translations}
      event={event}
      active="reports"
      searchParams={{}}
    >
      {reports.map((report) => (
        <Report
          key={report.slug}
          report={report}
          timezone={timezone}
          locale={locale}
        />
      ))}
    </ProgramAdminView>
  );
}
