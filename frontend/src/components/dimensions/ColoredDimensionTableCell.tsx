import type { ReactNode } from "react";
import { makeColorTranslucent } from "./helpers";
import type { Dimension } from "./models";
import { validateCachedDimensions } from "./models";

interface Props {
  // TODO move typing to codegen.ts (backend must specify scalar type)
  // cachedDimensions?: CachedDimensions;
  cachedDimensions?: unknown;
  dimension: Dimension;
  children?: ReactNode;
}

export default function ColoredDimensionTableCell(props: Props) {
  const { cachedDimensions, dimension, children } = props;
  let backgroundColor: string | undefined = undefined;

  if (cachedDimensions) {
    validateCachedDimensions(cachedDimensions);

    const firstValueSlug = cachedDimensions[dimension.slug]?.[0] || "";
    const valueColor = dimension.values.find(
      (value) => value.slug === firstValueSlug,
    )?.color;
    backgroundColor = valueColor ? makeColorTranslucent(valueColor) : undefined;
  }

  return (
    <td scope="row" className="align-middle" style={{ backgroundColor }}>
      {children}
    </td>
  );
}
