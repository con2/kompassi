import { ReactNode } from "react";
import { Column } from "../DataTable";

export function textMutedWhenInactive<T extends { isActive?: boolean }>(
  this: Column<T>,
  row: T,
  children?: ReactNode,
) {
  const className = row.isActive
    ? this.className
    : `${this.className} text-muted`;

  return (
    <td scope={this.scope} className={className}>
      {children}
    </td>
  );
}
