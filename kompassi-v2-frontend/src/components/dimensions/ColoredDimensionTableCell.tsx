import type { ReactNode } from "react";
import { Column } from "@con2/components";
import { makeColorTranslucent } from "@con2/components/helpers";
import { getDimensionValueTitle } from "./helpers";
import { validateCachedDimensions } from "./models";
import { graphql } from "@/__generated__";
import { ColoredDimensionTableCellFragment } from "@/__generated__/graphql";

graphql(`
  fragment ColoredDimensionTableCell on FullDimensionType {
    slug
    title(lang: $locale)
    isKeyDimension
    isTechnical
    isMultiValue
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
  dimension: ColoredDimensionTableCellFragment;
  children?: ReactNode;
}

// XXX any with sugar on top
interface HasCachedDimensions {
  cachedDimensions?: unknown | null;
}

export function buildKeyDimensionColumns<T extends HasCachedDimensions>(
  dimensions: ColoredDimensionTableCellFragment[],
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
