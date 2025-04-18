import { Choice, MultiSelect, SingleSelect } from "../forms/models";
import type { Dimension } from "./models";
import { validateCachedDimensions } from "./models";
import type { DimensionFilterInput } from "@/__generated__/graphql";

const reservedFilterNames = ["favorited", "past", "display", "search"];

/// Helper to build turn search params into dimension filters that you can pass into GraphQL
export function buildDimensionFilters(
  searchParams: Record<string, string>,
): DimensionFilterInput[] {
  return Object.entries(searchParams)
    .filter(([_, value]) => value.length)
    .filter(([name]) => !reservedFilterNames.includes(name))
    .map(([dimension, value]) => ({
      dimension,
      values: [value],
    }));
}

export function buildDimensionChoices(
  dimension: Dimension,
  includeEmptyChoice: boolean = false,
): Choice[] {
  const choices = dimension.values.map((value) => ({
    slug: value.slug,
    title: value.title ?? value.slug,
  }));

  if (includeEmptyChoice) {
    choices.unshift({
      slug: "",
      title: "",
    });
  }

  return choices;
}

/// For subjects using the cached dimensions protocol, this helper will return the
/// formatted dimension value for a given dimension. Multiple values will look like "Foo, Bar".
export function getDimensionValueTitle(
  dimension: Dimension,
  cachedDimensions: unknown,
) {
  validateCachedDimensions(cachedDimensions);

  const valueSlugs = cachedDimensions[dimension.slug] ?? [];
  const dimensionValues = dimension.values.filter((value) =>
    valueSlugs.includes(value.slug),
  );
  return dimensionValues.map((value) => value.title).join(", ");
}

export function buildDimensionField(
  dimension: Dimension,
  cachedDimensions: unknown,
  technicalDimensions: "omit" | "readonly" | "editable" = "omit",
) {
  validateCachedDimensions(cachedDimensions);

  const valueList = cachedDimensions[dimension.slug] ?? [];
  let type = dimension.isMultiValue ? "MultiSelect" : "SingleSelect";
  if (type === "SingleSelect" && valueList.length > 1) {
    console.warn(
      "SingleSelect was requested but multiple values were already set.",
      { dimension, cachedDimensions },
    );
    type = "MultiSelect";
  }

  const value = type === "SingleSelect" ? valueList[0] ?? "" : valueList;
  const readOnly = technicalDimensions === "readonly" && dimension.isTechnical;

  const field: SingleSelect | MultiSelect =
    type === "SingleSelect"
      ? {
          slug: dimension.slug,
          type: "SingleSelect",
          presentation: "dropdown",
          title: dimension.title ?? dimension.slug,
          choices: buildDimensionChoices(dimension),
          readOnly,
        }
      : {
          slug: dimension.slug,
          type: "MultiSelect",
          title: dimension.title ?? dimension.slug,
          choices: buildDimensionChoices(dimension),
          readOnly,
        };

  return { field, value };
}

export function buildDimensionValueSelectionForm(
  dimensions: Dimension[],
  cachedDimensions: unknown,
  technicalDimensions: "omit" | "readonly" | "editable" = "omit",
) {
  if (technicalDimensions === "omit") {
    dimensions = dimensions.filter((dimension) => !dimension.isTechnical);
  }

  const fieldsValues = dimensions.map((dimension) =>
    buildDimensionField(dimension, cachedDimensions),
  );
  const fields = fieldsValues.map(({ field }) => field);
  const values: Record<string, any> = {};
  fieldsValues.forEach(({ field, value }) => {
    values[field.slug] = value;
  });

  return { fields, values };
}

export function makeColorTranslucent(color: string) {
  return `color-mix(in srgb, ${color}, transparent 85%)`;
}

export function makeBadgeBackgroundColor(color: string) {
  return `color-mix(in srgb, ${color}, var(--bs-secondary) 50%)`;
}
