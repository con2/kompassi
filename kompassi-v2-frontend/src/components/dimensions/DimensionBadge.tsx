import { ColorBadge } from "@con2/components";
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
    <ColorBadge
      key={sdv.dimension.slug}
      color={sdv.value.color}
      title={sdv.dimension.title || sdv.dimension.slug}
    >
      {sdv.value.title}
    </ColorBadge>
  );
}
