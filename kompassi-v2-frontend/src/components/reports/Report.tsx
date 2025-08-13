import { Temporal } from "@js-temporal/polyfill";

import { graphql } from "@/__generated__";
import { ReportFragment, TypeOfColumn } from "@/__generated__/graphql";
import { Column, DataTable } from "@/components/DataTable";
import { formatDateTime } from "@/components/FormattedDateTime";
import { timezone as defaultTimezone } from "@/config";
import formatMoney from "@/helpers/formatMoney";
import { defaultLanguage } from "@/translations";
import { Card, CardBody, CardTitle } from "react-bootstrap";

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
  timezone: Temporal.TimeZoneLike = defaultTimezone,
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
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (_e) {
        return value as string;
      }
    default:
      const exhaustiveCheck: never = type;
      throw new Error(`Unimplemented column type: ${exhaustiveCheck}`);
  }
}

interface Props {
  report: ReportFragment;
  timezone: Temporal.TimeZoneLike;
  locale: string;
}

export default function Report({ report, timezone, locale }: Props) {
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
