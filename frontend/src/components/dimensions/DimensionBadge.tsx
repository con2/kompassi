import { makeBadgeBackgroundColor } from "./helpers";
import { graphql } from "@/__generated__";
import { DimensionBadgeFragment } from "@/__generated__/graphql";

graphql(`
  fragment DimensionBadge on ResponseDimensionValueType {
    dimension {
      slug
      title(lang: $locale)
    }

    value {
      slug
      title(lang: $locale)
      color
    }
  }
`);

interface Props {
  dimension: DimensionBadgeFragment;
}

export default function DimensionBadge({ dimension }: Props) {
  return (
    <span
      key={dimension.dimension.slug}
      className="badge ms-1"
      style={{
        backgroundColor:
          dimension.value.color &&
          makeBadgeBackgroundColor(dimension.value.color),
      }}
    >
      {dimension.value.title}
    </span>
  );
}
