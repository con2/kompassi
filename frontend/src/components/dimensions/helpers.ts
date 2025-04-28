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

export function makeColorTranslucent(color: string) {
  return `color-mix(in srgb, ${color}, transparent 85%)`;
}

export function makeBadgeBackgroundColor(color: string) {
  return `color-mix(in srgb, ${color}, var(--bs-secondary) 50%)`;
}
