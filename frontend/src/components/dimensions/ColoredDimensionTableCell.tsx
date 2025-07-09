import type { ReactNode } from "react";
import { Column } from "../DataTable";
import { getDimensionValueTitle, makeColorTranslucent } from "./helpers";
import type { Dimension } from "./models";
import { validateCachedDimensions } from "./models";
import { graphql } from "@/__generated__";
import { ColoredKeyDimensionTableCellFragment } from "@/__generated__/graphql";

graphql(`
  fragment ColoredKeyDimensionTableCell on FullDimensionType {
    slug
    title(lang: $locale)
    isKeyDimension
    values(lang: $locale) {
      slug
      title(lang: $locale)
      color
    }
  }
`);

interface Props {
  // TODO move typing to codegen.ts (backend must specify scalar type)
  // cachedDimensions?: CachedDimensions;
  cachedDimensions?: unknown;
  dimension: ColoredKeyDimensionTableCellFragment;
  children?: ReactNode;
}

// XXX any with sugar on top
interface ResponseLike {
  cachedDimensions?: unknown | null;
}

export function buildKeyDimensionColumns<T extends ResponseLike>(
  dimensions: ColoredKeyDimensionTableCellFragment[],
): Column<T>[] {
  return dimensions
    .filter((dimension) => dimension.isKeyDimension)
    .map((keyDimension) => ({
      slug: `keyDimensions.${keyDimension.slug}`,
      title: keyDimension.title ?? "",
      getCellElement: (row, children) => (
        <ColoredDimensionTableCell
          cachedDimensions={row.cachedDimensions}
          dimension={keyDimension}
        >
          {children}
        </ColoredDimensionTableCell>
      ),
      getCellContents: (row) =>
        getDimensionValueTitle(keyDimension, row.cachedDimensions),
    }));
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
