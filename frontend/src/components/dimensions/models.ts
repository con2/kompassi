// | null | undefined to make it easier to work with GraphQL
export interface DimensionValue {
  slug: string;
  title?: string | null;
  color?: string | null;
}

export interface Dimension {
  slug: string;
  title?: string | null;
  isMultiValue?: boolean;
  isTechnical?: boolean;
  isKeyDimension?: boolean;
  values: DimensionValue[];
}

export type CachedDimensions = Record<string, string[]>;

export function validateCachedDimensions(
  it: unknown,
): asserts it is CachedDimensions {
  // TODO
}
