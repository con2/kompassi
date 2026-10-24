import { Temporal } from "@js-temporal/polyfill";

import { ReportFragment, TypeOfColumn } from "@/__generated__/graphql";

function escapeCsvField(value: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }
  const str = "" + value;
  return /[",\r\n]/.test(str) ? `"${str.replace(/"/g, '""')}"` : str;
}

/**
 * Raw values rather than the formatted ones shown in the table, so that
 * spreadsheets can treat numbers and times as such. The total row is left out
 * so it does not get summed along with the data.
 */
export function reportToCsv(report: ReportFragment): string {
  const lines = [
    report.columns.map((column) => column.title),
    ...report.rows.map((row: unknown[]) => row),
  ].map((row) => row.map(escapeCsvField).join(","));

  // BOM so that Excel detects UTF-8 and shows ä and ö correctly
  return "﻿" + lines.join("\r\n") + "\r\n";
}

function formatFilenameTime(
  instant: Temporal.Instant,
  timezone: Temporal.TimeZoneLike,
): string {
  const zoned = instant.toZonedDateTimeISO(timezone);
  const pad = (n: number) => n.toString().padStart(2, "0");
  return (
    `${zoned.year}-${pad(zoned.month)}-${pad(zoned.day)}` +
    `T${pad(zoned.hour)}${pad(zoned.minute)}`
  );
}

function parseInstant(value: unknown): Temporal.Instant | null {
  if (typeof value !== "string") {
    return null;
  }
  try {
    return Temporal.Instant.from(value);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
  } catch (_e) {
    // eg. the "Not exchanged" row of ticket_exchange_by_hour
    return null;
  }
}

/**
 * Reports with a datetime column are named after the first and last time in it,
 * eg. ropecon2026_ticket_exchange_by_hour_2026-07-24T1000_2026-07-26T1800.csv.
 * Other reports cover everything up to the moment of export,
 * eg. ropecon2026_ticket_exchange_by_product_until_2026-10-24T1530.csv.
 */
export function reportCsvFilename(
  report: ReportFragment,
  filenamePrefix: string,
  timezone: Temporal.TimeZoneLike,
  now: Temporal.Instant = Temporal.Now.instant(),
): string {
  const datetimeColumnIndex = report.columns.findIndex(
    (column) => column.type === TypeOfColumn.Datetime,
  );
  const instants =
    datetimeColumnIndex >= 0
      ? report.rows
          .map((row: unknown[]) => parseInstant(row[datetimeColumnIndex]))
          .filter((instant): instant is Temporal.Instant => instant !== null)
          .sort(Temporal.Instant.compare)
      : [];

  const timeRange =
    instants.length > 0
      ? `${formatFilenameTime(instants[0], timezone)}_${formatFilenameTime(instants[instants.length - 1], timezone)}`
      : `until_${formatFilenameTime(now, timezone)}`;

  return `${filenamePrefix}_${report.slug}_${timeRange}.csv`;
}
