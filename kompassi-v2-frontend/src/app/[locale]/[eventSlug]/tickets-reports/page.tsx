import { SignInRequired } from "@con2/components";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { PaymentProvider, ReportFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import Report from "@/components/reports/Report";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import { timezone as defaultTimezone } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query TicketsAdminReportsPage($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      tickets {
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
  const t = translations.Tickets;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: t.admin.tabs.reports,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ReportsPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
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
    variables: { locale, eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const timezone = event.timezone || defaultTimezone;

  // HACK Translate provider id clientside
  const reports = JSON.parse(
    JSON.stringify(data.event.tickets.reports),
  ) as ReportFragment[];
  const salesByProviderReport = reports.find(
    (report) => report.slug === "sales_by_payment_provider",
  );
  if (salesByProviderReport) {
    salesByProviderReport.rows = salesByProviderReport.rows.map((row) => {
      const [provider_id, ...rest]: [PaymentProvider, ...any[]] = row as any;
      return [
        translations.Tickets.Order.attributes.provider.choices[provider_id],
        ...rest,
      ];
    });
  }

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      active="reports"
    >
      {reports.map((report) => (
        <Report
          key={report.slug}
          report={report}
          timezone={timezone}
          locale={locale}
        />
      ))}
    </TicketsAdminView>
  );
}
