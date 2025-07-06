import { makeBadgeBackgroundColor } from "./helpers";
import { graphql } from "@/__generated__";

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
  subjectDimensionValue: {
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

export default function DimensionBadge({ subjectDimensionValue: sdv }: Props) {
  return (
    <span
      key={sdv.dimension.slug}
      className="badge ms-2"
      title={sdv.dimension.title || sdv.dimension.slug}
      style={{
        backgroundColor: sdv.value.color
          ? makeBadgeBackgroundColor(sdv.value.color)
          : "var(--bs-secondary)",
      }}
    >
      {sdv.value.title}
    </span>
  );
}
