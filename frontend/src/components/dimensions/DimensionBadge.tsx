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
  dimension: {
    dimension: {
      slug: string;
      title?: string | null;
    };

    value: {
      slug: string;
      title?: string | null;
      color?: string | null;
    };
  };
}

export default function DimensionBadge({ dimension }: Props) {
  return (
    <span
      key={dimension.dimension.slug}
      className="badge ms-2"
      title={dimension.dimension.title || dimension.dimension.slug}
      style={{
        backgroundColor: dimension.value.color
          ? makeBadgeBackgroundColor(dimension.value.color)
          : "var(--bs-secondary)",
      }}
    >
      {dimension.value.title}
    </span>
  );
}
