import { notFound } from "next/navigation";

import { Card, CardBody, CardTitle } from "react-bootstrap";
import { graphql } from "@/__generated__";
import { ReportFragment, TypeOfColumn } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import { decodeBoolean } from "@/helpers/decodeBoolean";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment Report on ReportType {
    slug
    title(lang: $locale)
    columns {
      slug
      title(lang: $locale)
      type
    }
    rows
  }
`);

const query = graphql(`
  query TicketsAdminReportsPage($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug

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

function formatCellValue(value: unknown, type: TypeOfColumn) {
  switch (type) {
    case TypeOfColumn.String:
      return "" + value;
    case TypeOfColumn.Int:
      return "" + value;
    case TypeOfColumn.Percentage:
      return "" + ((value as number) * 100).toFixed(2) + "%";
  }
}

function Report({ report }: { report: ReportFragment }) {
  const firstColumnWidth = 12 - 2 * (report.columns.length - 1);

  const columns: Column<any>[] = report.columns.map((column, ind) => ({
    slug: column.slug,
    title: column.title,
    className: ind === 0 ? `col-${firstColumnWidth}` : "col-2 text-end",
    getCellContents: (row) => formatCellValue(row[ind], column.type),
  }));

  return (
    <Card className="mt-3 mb-3">
      <CardBody>
        <CardTitle>{report.title}</CardTitle>
        <DataTable columns={columns} rows={report.rows} />
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
  const reports = data.event.tickets.reports;

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      active="reports"
    >
      {reports.map((report) => (
        <Report key={report.slug} report={report} />
      ))}
    </TicketsAdminView>
  );
}
