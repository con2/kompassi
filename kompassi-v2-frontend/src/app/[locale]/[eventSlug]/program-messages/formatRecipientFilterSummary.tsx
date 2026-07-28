import { DimensionValueSelectFragment } from "@/__generated__/graphql";

interface FilterItem {
  dimension: string;
  values?: string[] | null;
}

/// Renders recipientFilters (OR of AND-groups) as a short human-readable summary,
/// eg. "(Type: Program host, State: Active) OR (Type: Program offer)".
export default function formatRecipientFilterSummary(
  groups: FilterItem[][],
  dimensions: DimensionValueSelectFragment[],
): string {
  if (groups.length === 0) {
    return "";
  }

  const dimensionsBySlug = new Map(dimensions.map((d) => [d.slug, d]));

  const groupSummaries = groups.map((group) => {
    const itemSummaries = group.map((item) => {
      const dimension = dimensionsBySlug.get(item.dimension);
      const dimensionTitle = dimension?.title ?? item.dimension;
      const valueTitles = (item.values ?? []).map((valueSlug) => {
        const value = dimension?.values.find((v) => v.slug === valueSlug);
        return value?.title ?? valueSlug;
      });
      return `${dimensionTitle}: ${valueTitles.join("/")}`;
    });
    return `(${itemSummaries.join(", ")})`;
  });

  return groupSummaries.join(" OR ");
}
