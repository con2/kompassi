import { CachedDimensions, Dimension } from "./models";

interface Props {
  dimension: Dimension;
  cachedDimensions: CachedDimensions;
}

/// Simple comma-separated list display of values of a single dimension.
export default function DimensionValues({
  dimension,
  cachedDimensions,
}: Props) {
  const values = cachedDimensions[dimension.slug] || [];
  if (values.length === 0) {
    return <></>;
  }

  const valuesBySlug = Object.fromEntries(
    dimension.values.map((value) => [value.slug, value]),
  );

  const title = values
    .map((value) => valuesBySlug[value])
    .filter(Boolean)
    .map((value) => value.title)
    .join(", ");

  return <>{title}</>;
}
