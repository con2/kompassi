"use client";

import { Temporal } from "@js-temporal/polyfill";
import { useCallback, useState, type ComponentProps } from "react";
import type { DayButtonProps } from "react-day-picker";
import { DayPicker } from "react-day-picker";
import { timezone } from "@/config";
import type { Translations } from "@/translations/en";

interface DateTimeInputProps {
  id?: string;
  name: string;
  defaultValue?: string;
  locale: string;
  messages: Translations["SchemaForm"];
  required?: boolean;
  readOnly?: boolean;
  dateRange?: { start: string; end: string };
}

function parseIsoToLocalDate(isoValue: string): Date {
  const zdt = Temporal.Instant.from(isoValue).toZonedDateTimeISO(timezone);
  return new Date(zdt.year, zdt.month - 1, zdt.day);
}

function parseIsoToTime(isoValue: string): string {
  const zdt = Temporal.Instant.from(isoValue).toZonedDateTimeISO(timezone);
  const h = String(zdt.hour).padStart(2, "0");
  const m = String(zdt.minute).padStart(2, "0");
  return `${h}:${m}`;
}

function formatDateForDisplay(date: Date, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

function toHiddenValue(date: Date | undefined, time: string): string {
  if (!date) return "";
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}T${time || "00:00"}`;
}

// Custom DayButton so we can apply btn-primary + text-white directly on the
// <button> element when selected. The `selected` classNames key targets the
// parent <td>, where Bootstrap's .btn re-declares --bs-btn-color (black),
// overriding any inherited value — so we must style the button itself.
function CalendarDayButton({
  day: _day,
  modifiers,
  className,
  ...props
}: DayButtonProps) {
  return (
    <button
      {...props}
      className={[
        className, // day_button base classes from classNames
        modifiers.selected ? "btn-primary text-white" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    />
  );
}

export default function DateTimeInput({
  id,
  name,
  defaultValue,
  locale,
  messages,
  required,
  readOnly,
  dateRange,
}: DateTimeInputProps) {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(() => {
    if (defaultValue) {
      try {
        return parseIsoToLocalDate(defaultValue);
      } catch {
        return undefined;
      }
    }
    return undefined;
  });

  const [time, setTime] = useState<string>(() => {
    if (defaultValue) {
      try {
        return parseIsoToTime(defaultValue);
      } catch {
        return "";
      }
    }
    return "";
  });

  const [calendarOpen, setCalendarOpen] = useState(false);

  const defaultMonth = (() => {
    if (selectedDate) return selectedDate;
    if (dateRange?.start) {
      try {
        return parseIsoToLocalDate(dateRange.start);
      } catch {
        return undefined;
      }
    }
    return undefined;
  })();

  const rangeStart = dateRange?.start
    ? (() => {
        try {
          return parseIsoToLocalDate(dateRange.start);
        } catch {
          return undefined;
        }
      })()
    : undefined;

  const rangeEnd = dateRange?.end
    ? (() => {
        try {
          return parseIsoToLocalDate(dateRange.end);
        } catch {
          return undefined;
        }
      })()
    : undefined;

  const isOutOfRange =
    selectedDate &&
    ((rangeStart && selectedDate < rangeStart) ||
      (rangeEnd && selectedDate > rangeEnd));

  const handleDaySelect = useCallback((day: Date | undefined) => {
    setSelectedDate(day);
    setCalendarOpen(false);
  }, []);

  const hiddenValue = toHiddenValue(selectedDate, time);

  return (
    <div style={{ position: "relative" }}>
      <div className="input-group">
        {/* Styled as a form-control so border colour and text colour match other inputs */}
        <button
          type="button"
          className="form-control text-start"
          style={{ width: "auto", flexGrow: 0, cursor: "pointer" }}
          onClick={() => setCalendarOpen((o) => !o)}
          disabled={readOnly}
          aria-expanded={calendarOpen}
          aria-haspopup="dialog"
          id={id}
        >
          {selectedDate ? formatDateForDisplay(selectedDate, locale) : "—"}
        </button>
        <input
          type="time"
          className="form-control"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          required={required && !selectedDate}
          readOnly={readOnly}
          style={{ maxWidth: "8em" }}
        />
      </div>

      {calendarOpen && !readOnly && (
        <div
          className="dropdown-menu show p-2"
          style={{ zIndex: 1000 }}
          role="dialog"
          aria-label="Date picker"
        >
          <DayPicker
            mode="single"
            selected={selectedDate}
            onSelect={handleDaySelect}
            defaultMonth={defaultMonth}
            ISOWeek
            formatters={{
              formatWeekdayName: (weekday) =>
                new Intl.DateTimeFormat(locale, { weekday: "short" }).format(
                  weekday,
                ),
              formatCaption: (month) =>
                new Intl.DateTimeFormat(locale, {
                  month: "long",
                  year: "numeric",
                }).format(month),
            }}
            components={{ DayButton: CalendarDayButton }}
            classNames={{
              root: "",
              months: "",
              // position-relative so the nav can be absolutely placed over the caption
              month: "position-relative",
              // px-4 keeps the month label clear of the absolutely positioned nav buttons
              month_caption: "text-center fw-semibold mb-2 px-4",
              caption_label: "",
              // nav is styled via the `styles` prop; reset class to avoid conflict
              nav: "",
              button_previous: "btn btn-sm btn-outline-secondary",
              button_next: "btn btn-sm btn-outline-secondary",
              weeks: "",
              week: "",
              weekdays: "",
              weekday: "text-center text-muted small",
              day: "",
              day_button: "btn btn-sm",
              today: "fw-bold",
              outside: "text-muted opacity-50",
              disabled: "text-muted opacity-25",
              hidden: "invisible",
            }}
            styles={{
              // Float the nav over the caption row, buttons at opposite ends
              nav: {
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                display: "flex",
                justifyContent: "space-between",
              },
              // Fixed cell widths so every column lines up regardless of content
              weekday: { width: "2.25rem", textAlign: "center" },
              day: { width: "2.25rem", textAlign: "center", padding: 0 },
              day_button: { width: "2.25rem", padding: 0, aspectRatio: "1" },
            }}
          />
        </div>
      )}

      <input type="hidden" name={name} value={hiddenValue} />

      {isOutOfRange && (
        <div className="text-warning small mt-1">
          {messages.warnings.dateOutOfRange}
        </div>
      )}
    </div>
  );
}
