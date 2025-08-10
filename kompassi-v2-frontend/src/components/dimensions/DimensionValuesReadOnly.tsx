import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import { CachedDimensions } from "./models";

interface Props {
  dimensions: DimensionValueSelectFragment[];
  cachedDimensions: CachedDimensions;
  className?: string;
  fieldClassName?: string;
}

export default function DimensionValuesReadOnly({
  dimensions,
  cachedDimensions,
  className = `row`,
  fieldClassName = `col-12 mb-3`,
}: Props) {
  return (
    <div className={className}>
      {dimensions
        .filter((dimension) => cachedDimensions[dimension.slug]?.length > 0)
        .map((dimension) => {
          const values = cachedDimensions[dimension.slug];
          const titleBySlug = Object.fromEntries(
            dimension.values.map((v) => [v.slug, v.title]),
          );
          return (
            <div key={dimension.slug} className={fieldClassName}>
              <div className="form-label fw-bold">{dimension.title}</div>
              {values.map((slug) => (
                <div key={slug}>{titleBySlug[slug] || slug}</div>
              ))}
            </div>
          );
        })}
    </div>
  );
}
