import { Temporal } from "@js-temporal/polyfill";
import { notFound } from "next/navigation";

import { Card, CardBody, CardTitle } from "react-bootstrap";
import { graphql } from "@/__generated__";
import {
  PaymentProvider,
  ReportFragment,
  TypeOfColumn,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import { formatDateTime } from "@/components/FormattedDateTime";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import { timezone as defaultTimezone } from "@/config";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { defaultLanguage, getTranslations } from "@/translations";

graphql(`
  fragment Report on ReportType {
    slug
    title(lang: $locale)
    footer(lang: $locale)
    columns {
      slug
      title(lang: $locale)
      type
    }
    rows
    totalRow
  }
`);

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
  params: {
    locale: string;
    eventSlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
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

const defaultOptions: Intl.DateTimeFormatOptions = {
  weekday: "short",
  month: "short",
  day: "numeric",
  year: "numeric",
  hour: "numeric",
  minute: "2-digit",
  hourCycle: "h23",
};

function formatCellValue(
  value: unknown,
  type: TypeOfColumn,
  timezone: Temporal.TimeZoneProtocol = defaultTimezone,
  locale: string = defaultLanguage,
  options: Intl.DateTimeFormatOptions = defaultOptions,
) {
  switch (type) {
    case TypeOfColumn.String:
      return "" + value;
    case TypeOfColumn.Int:
      return "" + value;
    case TypeOfColumn.Percentage:
      return "" + ((value as number) * 100).toFixed(1) + "%";
    case TypeOfColumn.Currency:
      return formatMoney(value as string);
    case TypeOfColumn.Datetime:
      try {
        return formatDateTime(value as string, locale, options, timezone);
      } catch (e) {
        return value as string;
      }
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unimplemented column type: ${exhaustiveCheck}`);
  }
}

interface ReportProps {
  report: ReportFragment;
  timezone: Temporal.TimeZoneProtocol;
  locale: string;
}

function Report({ report, timezone, locale }: ReportProps) {
  const firstColumnWidth = 12 - 2 * (report.columns.length - 1);
  function cellClassName(column: Column<any>, index: number) {
    return index === 0 ? `col-${firstColumnWidth}` : "col-2 text-end";
  }

  const columns: Column<any>[] = report.columns.map((column, ind) => ({
    slug: column.slug,
    title: column.title,
    className: cellClassName(column, ind),
    getCellContents: (row) =>
      formatCellValue(row[ind], column.type, timezone, locale),
  }));

  return (
    <Card className="mt-3 mb-3">
      <CardBody>
        <CardTitle>{report.title}</CardTitle>
        <DataTable columns={columns} rows={report.rows}>
          {report.totalRow && (
            <tfoot>
              <tr>
                {report.columns.map((column, ind) => (
                  <th key={ind} className={cellClassName(column, ind)}>
                    {formatCellValue(
                      report.totalRow![ind],
                      column.type,
                      timezone,
                      locale,
                    )}
                  </th>
                ))}
              </tr>
            </tfoot>
          )}
        </DataTable>
        {report.footer && <div className="mt-3 form-text">{report.footer}</div>}
      </CardBody>
    </Card>
  );
}

export default async function ReportsPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const timezone = Temporal.TimeZone.from(event.timezone || "UTC");

  // HACK
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
