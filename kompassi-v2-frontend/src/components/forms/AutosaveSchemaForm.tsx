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

function withoutFileUploads(fields: Field[]): Field[] {
  return fields.filter((field) => field.type !== "FileUpload");
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

  useEffect(() => {
    if (draftKey) pruneExpiredDrafts();
  }, [draftKey]);

  useEffect(() => {
    if (!draftKey) return;
    const form = containerRef.current?.closest("form");
    if (!form) return;

    let timer: ReturnType<typeof setTimeout> | undefined;
    const save = () => {
      timer = undefined;
      const formData = new FormData(form);
      saveDraft(
        draftKey,
        processFormData(withoutFileUploads(fields), formData),
      );
    };
    const saveLater = () => {
      if (timer) clearTimeout(timer);
      timer = setTimeout(save, saveDelayMs);
    };
    const saveNow = () => {
      if (timer) clearTimeout(timer);
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
      if (timer) clearTimeout(timer);
      form.removeEventListener("input", saveLater);
      form.removeEventListener("change", saveLater);
      form.removeEventListener("click", saveLater);
      form.removeEventListener("submit", saveNow);
      window.removeEventListener("pagehide", saveNow);
    };
  }, [draftKey, fields]);

  const discard = useCallback(() => {
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
