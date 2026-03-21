"use client";

import { Temporal } from "@js-temporal/polyfill";
import { useCallback, useState } from "react";
import { DayPicker } from "react-day-picker";
import { timezone } from "@/config";

interface DateTimeInputProps {
  id?: string;
  name: string;
  defaultValue?: string;
  locale: string;
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

export default function DateTimeInput({
  id,
  name,
  defaultValue,
  locale,
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
        <button
          type="button"
          className="btn btn-outline-secondary"
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
            classNames={{
              root: "",
              months: "d-flex gap-2",
              month: "",
              month_caption: "d-flex justify-content-center mb-2 fw-semibold",
              caption_label: "",
              nav: "d-flex justify-content-between mb-1",
              button_previous: "btn btn-sm btn-outline-secondary",
              button_next: "btn btn-sm btn-outline-secondary",
              weeks: "",
              week: "d-flex",
              weekdays: "d-flex",
              weekday: "text-center text-muted small",
              day: "",
              day_button: "btn btn-sm",
              selected: "btn btn-primary btn-sm",
              today: "fw-bold",
              outside: "text-muted opacity-50",
              disabled: "text-muted opacity-25",
              hidden: "invisible",
            }}
          />
        </div>
      )}

      <input type="hidden" name={name} value={hiddenValue} />

      {isOutOfRange && (
        <div className="text-warning small mt-1">
          Selected date is outside the event date range.
        </div>
      )}
    </div>
  );
}
