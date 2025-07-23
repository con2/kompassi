import { graphql } from "@/__generated__";

graphql(`
  fragment DimensionFilterValue on DimensionValueType {
    slug
    title(lang: $locale)
  }
`);

graphql(`
  fragment DimensionFilter on FullDimensionType {
    slug
    title(lang: $locale)
    isMultiValue
    isListFilter
    isKeyDimension
    values(lang: $locale) {
      ...DimensionFilterValue
    }
  }
`);

export type CachedDimensions = Record<string, string[]>;

export function validateCachedDimensions(
  it: unknown,
): asserts it is CachedDimensions {
  // TODO
}
