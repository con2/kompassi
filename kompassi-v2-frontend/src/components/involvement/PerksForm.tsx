"use client";

import { useMemo, useState, useTransition } from "react";
import {
  AnnotationDataType,
  AnnotationsFormAnnotationFragment,
  DimensionValueSelectFragment,
} from "@/__generated__/graphql";
import {
  annotationOverrideValue,
  dimensionOverrideValue,
  PerksOverridePayload,
} from "@/components/involvement/perks";
import type { Translations } from "@/translations/en";

type CombinedPerksMessages =
  Translations["Involvement"]["attributes"]["combinedPerks"];

interface DimensionPerk {
  kind: "dimension";
  key: string;
  overrideValue: string;
  title: string;
  dimension: DimensionValueSelectFragment;
}

interface AnnotationPerk {
  kind: "annotation";
  key: string;
  overrideValue: string;
  title: string;
  annotation: AnnotationsFormAnnotationFragment;
}

type Perk = DimensionPerk | AnnotationPerk;

interface Props {
  /** All involvement dimensions; technical ones are filtered out as non-perks. */
  dimensions: DimensionValueSelectFragment[];
  /** Perk annotations (perksOnly); computed ones are filtered out. */
  annotations: AnnotationsFormAnnotationFragment[];
  cachedDimensions: Record<string, string[]>;
  cachedAnnotations: Record<string, string | number | boolean>;
  /** Values of the manual-perks-override dimension (`d-…` / `a-…`). */
  manualPerksOverride: string[];
  messages: CombinedPerksMessages;
  schemaFormMessages: Translations["SchemaForm"];
  onSubmit: (payload: PerksOverridePayload) => Promise<void>;
}

/** State value for a single perk: dimension slugs or a stringified annotation value. */
type PerkValue = string | string[];

function initialDimensionValue(
  dimension: DimensionValueSelectFragment,
  cachedDimensions: Record<string, string[]>,
): PerkValue {
  const values = cachedDimensions[dimension.slug] ?? [];
  return dimension.isMultiValue ? values : values[0] ?? "";
}

function initialAnnotationValue(
  annotation: AnnotationsFormAnnotationFragment,
  cachedAnnotations: Record<string, string | number | boolean>,
): PerkValue {
  const value = cachedAnnotations[annotation.slug];
  if (annotation.type === AnnotationDataType.Boolean) {
    return value === true ? "true" : value === false ? "false" : "";
  }
  return value == null ? "" : String(value);
}

/**
 * Lets an Involvement admin manually override individual perks (dimension values and
 * annotation values) of a person's combined perks. Each perk has its own value control
 * and an Override checkbox; unticked perks are recomputed by the Emperkelator on save.
 *
 * Deliberately a self-contained form rather than reusing SchemaForm, as interleaving the
 * per-perk override controls would require intrusive changes to SchemaForm/SchemaFormInput.
 */
export default function PerksForm({
  dimensions,
  annotations,
  cachedDimensions,
  cachedAnnotations,
  manualPerksOverride,
  messages,
  schemaFormMessages,
  onSubmit,
}: Props) {
  const perks: Perk[] = useMemo(() => {
    const dimensionPerks: Perk[] = dimensions
      .filter((dimension) => !dimension.isTechnical)
      .map((dimension) => ({
        kind: "dimension",
        key: `d:${dimension.slug}`,
        overrideValue: dimensionOverrideValue(dimension.slug),
        title: dimension.title ?? dimension.slug,
        dimension,
      }));
    const annotationPerks: Perk[] = annotations
      .filter((annotation) => !annotation.isComputed)
      .map((annotation) => ({
        kind: "annotation",
        key: `a:${annotation.slug}`,
        overrideValue: annotationOverrideValue(annotation.slug),
        title: annotation.title ?? annotation.slug,
        annotation,
      }));
    return [...dimensionPerks, ...annotationPerks];
  }, [dimensions, annotations]);

  const [overridden, setOverridden] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(
      perks.map((perk) => [
        perk.overrideValue,
        manualPerksOverride.includes(perk.overrideValue),
      ]),
    ),
  );
  const [values, setValues] = useState<Record<string, PerkValue>>(() =>
    Object.fromEntries(
      perks.map((perk) => [
        perk.key,
        perk.kind === "dimension"
          ? initialDimensionValue(perk.dimension, cachedDimensions)
          : initialAnnotationValue(perk.annotation, cachedAnnotations),
      ]),
    ),
  );
  const [isPending, startTransition] = useTransition();

  function setValue(key: string, value: PerkValue) {
    setValues((previous) => ({ ...previous, [key]: value }));
  }

  function handleSubmit() {
    const payload: PerksOverridePayload = {
      overrides: [],
      dimensions: {},
      annotations: {},
    };

    for (const perk of perks) {
      if (!overridden[perk.overrideValue]) {
        continue;
      }
      payload.overrides.push(perk.overrideValue);

      if (perk.kind === "dimension") {
        const value = values[perk.key];
        payload.dimensions[perk.dimension.slug] = perk.dimension.isMultiValue
          ? (value as string[])
          : value
            ? [value as string]
            : [];
      } else {
        const value = values[perk.key] as string;
        const { type, slug } = perk.annotation;
        if (type === AnnotationDataType.Number) {
          if (value !== "") {
            payload.annotations[slug] = Number(value);
          }
        } else if (type === AnnotationDataType.Boolean) {
          if (value === "true" || value === "false") {
            payload.annotations[slug] = value === "true";
          }
        } else {
          payload.annotations[slug] = value;
        }
      }
    }

    startTransition(async () => {
      await onSubmit(payload);
    });
  }

  function renderControl(perk: Perk, disabled: boolean) {
    const inputId = `perk-${perk.overrideValue}`;

    if (perk.kind === "dimension") {
      const { dimension } = perk;
      if (dimension.isMultiValue) {
        const selected = (values[perk.key] as string[]) ?? [];
        return dimension.values.map((choice) => {
          const choiceId = `${inputId}-${choice.slug}`;
          return (
            <div className="form-check" key={choice.slug}>
              <input
                className="form-check-input"
                type="checkbox"
                id={choiceId}
                disabled={disabled}
                checked={selected.includes(choice.slug)}
                onChange={(event) =>
                  setValue(
                    perk.key,
                    event.target.checked
                      ? [...selected, choice.slug]
                      : selected.filter((slug) => slug !== choice.slug),
                  )
                }
              />
              <label className="form-check-label" htmlFor={choiceId}>
                {choice.title ?? choice.slug}
              </label>
            </div>
          );
        });
      }

      return (
        <select
          className="form-select"
          id={inputId}
          disabled={disabled}
          value={values[perk.key] as string}
          onChange={(event) => setValue(perk.key, event.target.value)}
        >
          <option value="">—</option>
          {dimension.values.map((choice) => (
            <option value={choice.slug} key={choice.slug}>
              {choice.title ?? choice.slug}
            </option>
          ))}
        </select>
      );
    }

    const { annotation } = perk;
    const value = values[perk.key] as string;

    switch (annotation.type) {
      case AnnotationDataType.Number:
        return (
          <input
            className="form-control"
            type="number"
            id={inputId}
            disabled={disabled}
            value={value}
            onChange={(event) => setValue(perk.key, event.target.value)}
          />
        );
      case AnnotationDataType.Boolean:
        return (
          <select
            className="form-select"
            id={inputId}
            disabled={disabled}
            value={value}
            onChange={(event) => setValue(perk.key, event.target.value)}
          >
            <option value="">—</option>
            <option value="true">{schemaFormMessages.boolean.true}</option>
            <option value="false">{schemaFormMessages.boolean.false}</option>
          </select>
        );
      default:
        return (
          <input
            className="form-control"
            type={
              annotation.type === AnnotationDataType.Datetime
                ? "datetime-local"
                : "text"
            }
            id={inputId}
            disabled={disabled}
            value={value}
            onChange={(event) => setValue(perk.key, event.target.value)}
          />
        );
    }
  }

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        handleSubmit();
      }}
    >
      {perks.map((perk) => {
        const isOverridden = !!overridden[perk.overrideValue];
        const checkboxId = `override-${perk.overrideValue}`;
        return (
          <div className="row mb-3 align-items-start" key={perk.overrideValue}>
            <label
              className="col-sm-3 col-form-label fw-bold"
              htmlFor={`perk-${perk.overrideValue}`}
            >
              {perk.title}
            </label>
            <div className="col-sm-5">{renderControl(perk, !isOverridden)}</div>
            <div className="col-sm-4">
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  id={checkboxId}
                  checked={isOverridden}
                  onChange={(event) =>
                    setOverridden((previous) => ({
                      ...previous,
                      [perk.overrideValue]: event.target.checked,
                    }))
                  }
                />
                <label className="form-check-label" htmlFor={checkboxId}>
                  {messages.override}
                </label>
              </div>
              <small className="text-muted">
                {isOverridden
                  ? messages.manuallyOverridden
                  : messages.automatic}
              </small>
            </div>
          </div>
        );
      })}

      <button type="submit" className="btn btn-primary" disabled={isPending}>
        {messages.saveButton}
      </button>
    </form>
  );
}
