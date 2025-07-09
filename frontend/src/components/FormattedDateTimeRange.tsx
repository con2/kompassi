import { Temporal } from "@js-temporal/polyfill";
import { formatDateTime } from "./FormattedDateTime";
import { timezone as defaultTimezone } from "@/config";

/// NOTE: scope and session are non-? but |undefined by design so that omitting them is a conscious decision
interface Props {
  locale: string;
  start: string | null | undefined; // ISO 8601 (2024-02-24T17:55:00Z)
  end: string | null | undefined; // ISO 8601 (2024-02-24T17:55:00Z)
  scope: {
    slug: string;
    timezone: string;
  }; // TODO(#436) event or organization
  session: unknown | undefined; // TODO(#436) from await auth()
  includeDuration?: boolean;
  options?: Intl.DateTimeFormatOptions;
}

const defaultOptions: Intl.DateTimeFormatOptions = {
  dateStyle: "full",
  timeStyle: "short",
};

// TODO(#436) proper handling of event & session time zones
export function isSameDay(start: string, end: string) {
  const startDateTime =
    Temporal.Instant.from(start).toZonedDateTimeISO(defaultTimezone);
  const endDateTime =
    Temporal.Instant.from(end).toZonedDateTimeISO(defaultTimezone);
  const startDay = startDateTime.toPlainDate();
  const endDay = endDateTime.toPlainDate();
  return startDay.equals(endDay);
}

export function formatDuration(start: string, end: string, locale: string) {
  const startDateTime =
    Temporal.Instant.from(start).toZonedDateTimeISO(defaultTimezone);
  const endDateTime =
    Temporal.Instant.from(end).toZonedDateTimeISO(defaultTimezone);
  const durationMinutes = startDateTime
    .until(endDateTime)
    .total({ unit: "minute" });

  return formatDurationMinutes(durationMinutes, locale);
}

export function formatDurationMinutes(durationMinutes: number, locale: string) {
  const hours = Math.floor(durationMinutes / 60);
  const minutes = durationMinutes % 60;

  if (hours > 0) {
    if (minutes > 0) {
      return `${hours} h ${minutes} min`;
    } else {
      return `${hours} h`;
    }
  } else {
    return `${minutes} min`;
  }
}

// TODO(#436) proper handling of event & session time zones
export default function FormattedDateTimeRange({
  start,
  end,
  scope,
  locale = "en",
  options = defaultOptions,
  includeDuration = false,
}: Props) {
  const timezone = scope.timezone
    ? Temporal.TimeZone.from(scope.timezone)
    : defaultTimezone;

  const formattedStart = start
    ? formatDateTime(start, locale, options, timezone)
    : "";

  const endOptions = {
    ...options,
    dateStyle:
      start && end && isSameDay(start, end) ? undefined : options.dateStyle,
  };
  const formattedEnd = end
    ? formatDateTime(end, locale, endOptions, timezone)
    : "";

  const formattedDuration =
    start && end && includeDuration ? formatDuration(start, end, locale) : "";

  return (
    <span>
      <time dateTime={start ?? undefined}>{formattedStart}</time>
      {" – "}
      <time dateTime={end ?? undefined}>{formattedEnd}</time>
      {formattedDuration && ` (${formattedDuration})`}
    </span>
  );
}
