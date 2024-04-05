import { Temporal } from "@js-temporal/polyfill";
import { formatDateTime } from "./FormattedDateTime";
import { timezone } from "@/config";

/// NOTE: scope and session are non-? but |undefined by design so that omitting them is a conscious decision
interface Props {
  locale: string;
  start: string | null | undefined; // ISO 8601 (2024-02-24T17:55:00Z)
  end: string | null | undefined; // ISO 8601 (2024-02-24T17:55:00Z)
  scope: unknown | undefined; // TODO(#436) event or organization
  session: unknown | undefined; // TODO(#436) from await auth()
  options?: Intl.DateTimeFormatOptions;
}

const defaultOptions: Intl.DateTimeFormatOptions = {
  dateStyle: "full",
  timeStyle: "short",
};

// TODO(#436) proper handling of event & session time zones
export function isSameDay(start: string, end: string) {
  const startDateTime =
    Temporal.Instant.from(start).toZonedDateTimeISO(timezone);
  const endDateTime = Temporal.Instant.from(end).toZonedDateTimeISO(timezone);
  const startDay = startDateTime.toPlainDate();
  const endDay = endDateTime.toPlainDate();
  return startDay.equals(endDay);
}

// TODO(#436) proper handling of event & session time zones
export default function FormattedDateTimeRange({
  start,
  end,
  locale = "en",
  options = defaultOptions,
}: Props) {
  const formattedStart = start ? formatDateTime(start, locale, options) : "";

  const endOptions = {
    ...options,
    dateStyle:
      start && end && isSameDay(start, end) ? undefined : ("full" as const),
  };
  const formattedEnd = end ? formatDateTime(end, locale, endOptions) : "";

  return (
    <span>
      <time dateTime={start ?? undefined}>{formattedStart}</time>
      {" – "}
      <time dateTime={end ?? undefined}>{formattedEnd}</time>
    </span>
  );
}
