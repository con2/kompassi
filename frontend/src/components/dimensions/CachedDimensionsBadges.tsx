import { Fragment } from "react";
import { makeBadgeBackgroundColor } from "./helpers";
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
                <span
                  key={value.slug}
                  className="badge ms-2"
                  title={dimension.title || dimension.slug}
                  style={{
                    backgroundColor: value.color
                      ? makeBadgeBackgroundColor(value.color)
                      : "var(--bs-secondary)",
                  }}
                >
                  {value.title || value.slug}
                </span>
              );
            })}
          </Fragment>
        );
      })}
    </>
  );
}
