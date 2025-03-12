import { Temporal } from "@js-temporal/polyfill";
import { timezone as defaultTimezone } from "@/config";

/// NOTE: scope and session are non-? but |undefined by design so that omitting them is a conscious decision
interface Props {
  locale: string;
  value: string | null | undefined; // ISO 8601 (2024-02-24T17:55:00Z)
  scope: unknown | undefined; // TODO(#436) event or organization
  session: unknown | undefined; // TODO(#436) from await auth()
  options?: Intl.DateTimeFormatOptions;
}

const defaultOptions: Intl.DateTimeFormatOptions = {
  dateStyle: "medium", // used to disambiguate day and month
  timeStyle: "short",
};

// TODO(#436) proper handling of event & session time zones
/// Convert a timestamp from the wire format (ISO 8601) to a human-readable string.
export function formatDateTime(
  value: string,
  locale: string,
  options: Intl.DateTimeFormatOptions = defaultOptions,
  timezone: Temporal.TimeZone | Temporal.TimeZoneProtocol = defaultTimezone,
) {
  return Temporal.Instant.from(value)
    .toZonedDateTimeISO(timezone)
    .toLocaleString(locale, options);
}

// TODO(#436) proper handling of event & session time zones
export default function FormattedDateTime({
  value,
  locale = "en",
  options = defaultOptions,
}: Props) {
  const formatted = value ? formatDateTime(value, locale, options) : "";
  return <time dateTime={value ?? undefined}>{formatted}</time>;
}
