import { Fragment } from "react";
import { ColorBadge } from "@con2/components";
import { validateCachedDimensions } from "./models";
import { graphql } from "@/__generated__";
import { CachedDimensionsBadgesFragment } from "@/__generated__/graphql";

graphql(`
  fragment CachedDimensionsBadges on FullDimensionType {
    slug
    title(lang: $locale)

    values(lang: $locale) {
      slug
      title(lang: $locale)
      color
    }
  }
`);

interface Props {
  dimensions: CachedDimensionsBadgesFragment[];
  cachedDimensions: unknown;
}

export default function CachedDimensionBadges({
  dimensions,
  cachedDimensions,
}: Props) {
  validateCachedDimensions(cachedDimensions);

  return (
    <>
      {dimensions.map((dimension) => {
        const valueSlugs = cachedDimensions[dimension.slug];
        if (!valueSlugs || valueSlugs.length === 0) {
          return null;
        }

        return (
          <Fragment key={dimension.slug}>
            {valueSlugs.map((valueSlug) => {
              const value = dimension.values.find((v) => v.slug === valueSlug);
              if (!value) {
                return null;
              }

              return (
                <ColorBadge
                  key={value.slug}
                  color={value.color}
                  title={dimension.title || dimension.slug}
                >
                  {value.title || value.slug}
                </ColorBadge>
              );
            })}
          </Fragment>
        );
      })}
    </>
  );
}
