"use client";

import { formatDateTime } from "@con2/components";
import { toZonedDateTime } from "@con2/components/helpers";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";

import {
  clearDraft,
  loadDraft,
  pruneExpiredDrafts,
  saveDraft,
} from "./formDraft";
import type { Field, Values } from "./models";
import processFormData from "./processFormData";
import { SchemaForm, type SchemaFormProps } from "./SchemaForm";

interface Props extends SchemaFormProps {
  /// Identifies the draft in localStorage. Pass null to disable autosaving, eg.
  /// for hard anonymous surveys whose answers should leave no trace.
  draftKey: string | null;
}

const saveDelayMs = 500;

/// Files cannot be restored into an input, and answers the backend encrypts
/// at rest must not sit in plaintext in localStorage.
function draftableFields(fields: Field[]): Field[] {
  return fields
    .filter((field) => field.type !== "FileUpload" && !field.encryptTo?.length)
    .map((field) =>
      field.type === "MultiItemField"
        ? { ...field, fields: draftableFields(field.fields) }
        : field,
    );
}

/// DateTimeInput submits a naive local datetime but only accepts a full
/// instant as defaultValue, so a saved value must be converted before restore.
function normalizeRestoredValues(fields: Field[], values: Values): Values {
  const normalized = { ...values };
  for (const field of fields) {
    const value = normalized[field.slug];
    if (field.type === "DateTimeField" && typeof value === "string" && value) {
      try {
        normalized[field.slug] = toZonedDateTime(value).toInstant().toString();
      } catch {
        delete normalized[field.slug];
      }
    } else if (
      field.type === "MultiItemField" &&
      value &&
      typeof value === "object" &&
      !Array.isArray(value)
    ) {
      normalized[field.slug] = normalizeRestoredValues(
        field.fields,
        value as Values,
      );
    }
  }
  return normalized;
}

const subscribeToNothing = () => () => {};

/// SchemaForm that keeps the user's input in localStorage until the enclosing
/// form has been submitted successfully. Clearing the draft is the job of the
/// page the submission redirects to (see ClearDraft).
export default function AutosaveSchemaForm(props: Props) {
  const { draftKey, fields, values, messages, locale } = props;

  // The draft is read only on the client and only after hydration, so the
  // server and the first client render agree on the markup.
  const isHydrated = useSyncExternalStore(
    subscribeToNothing,
    () => true,
    () => false,
  );
  const restored = useMemo(
    () => (isHydrated && draftKey ? loadDraft(draftKey) : null),
    [isHydrated, draftKey],
  );
  const [discarded, setDiscarded] = useState(false);
  const draft = discarded ? null : restored;

  const containerRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  // What the form showed right after its last mount. A save that would store
  // exactly this is skipped: it would only turn an untouched or just-discarded
  // form into a draft (the discard click and a later pagehide both trigger a
  // save).
  const baselineRef = useRef<string | null>(null);

  const serializeForm = useCallback(
    (form: HTMLFormElement) =>
      JSON.stringify(
        processFormData(draftableFields(fields), new FormData(form)),
      ),
    [fields],
  );

  useEffect(() => {
    if (draftKey) pruneExpiredDrafts();
  }, [draftKey]);

  useEffect(() => {
    const form = containerRef.current?.closest("form");
    baselineRef.current = form ? serializeForm(form) : null;
  }, [draft, serializeForm]);

  useEffect(() => {
    if (!draftKey) return;
    const form = containerRef.current?.closest("form");
    if (!form) return;

    const cancelPending = () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = undefined;
    };
    const save = () => {
      timerRef.current = undefined;
      const serialized = serializeForm(form);
      if (serialized === baselineRef.current) return;
      saveDraft(draftKey, JSON.parse(serialized));
    };
    const saveLater = () => {
      cancelPending();
      timerRef.current = setTimeout(save, saveDelayMs);
    };
    const saveNow = () => {
      cancelPending();
      save();
    };

    // click covers inputs that update a hidden field programmatically
    // (DateTimeInput), which fires no input or change event on the form.
    form.addEventListener("input", saveLater);
    form.addEventListener("change", saveLater);
    form.addEventListener("click", saveLater);
    form.addEventListener("submit", saveNow);
    window.addEventListener("pagehide", saveNow);
    return () => {
      cancelPending();
      form.removeEventListener("input", saveLater);
      form.removeEventListener("change", saveLater);
      form.removeEventListener("click", saveLater);
      form.removeEventListener("submit", saveNow);
      window.removeEventListener("pagehide", saveNow);
    };
  }, [draftKey, serializeForm]);

  const discard = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = undefined;
    if (draftKey) clearDraft(draftKey);
    setDiscarded(true);
  }, [draftKey]);

  const effectiveValues = useMemo(
    () =>
      draft
        ? { ...values, ...normalizeRestoredValues(fields, draft.values) }
        : values,
    [draft, fields, values],
  );

  if (!draftKey) {
    return <SchemaForm {...props} />;
  }

  return (
    <div ref={containerRef}>
      {draft && (
        <div className="alert alert-info d-flex align-items-center justify-content-between gap-3">
          <span>
            {messages.draft.restored.replace(
              "{savedAt}",
              formatDateTime(draft.savedAt, locale ?? "fi"),
            )}
          </span>
          <button
            type="button"
            className="btn btn-sm btn-outline-secondary flex-shrink-0"
            onClick={discard}
          >
            {messages.draft.discard}
          </button>
        </div>
      )}
      <SchemaForm
        key={draft ? "restored" : "original"}
        {...props}
        values={effectiveValues}
      />
    </div>
  );
}
