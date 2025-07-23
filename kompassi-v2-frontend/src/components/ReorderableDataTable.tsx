"use client";

import { Reorder, useDragControls } from "motion/react";
import { ReactNode, Fragment } from "react";

export interface Column<Row> {
  slug: string;
  title: ReactNode;
  getCellElement?: (row: Row, children?: ReactNode) => ReactNode;
  getCellContents?: (row: Row) => ReactNode;
  getHeaderElement?: (children?: ReactNode) => ReactNode;
  getHeaderContents?: () => ReactNode;
  className?: string;
  scope?: string;
}

interface DataTableProps<Row> {
  className?: string;
  rows: Row[];
  columns: Column<Row>[];
  getTotalMessage?: (total: number) => ReactNode;

  /// By default, first column (0) is designated scope="row". Set to -1 to disable.
  children?: ReactNode;

  onReorderRows: (rows: Row[]) => void;
  keyColumn: keyof Row;
  messages: {
    dragToReorder: string;
  };
}

function defaultCellElement<Row>(
  this: Column<Row>,
  _row: Row,
  children?: ReactNode,
) {
  if (this.scope === "row") {
    return (
      <th scope={this.scope} className={this.className}>
        {children}
      </th>
    );
  } else {
    return (
      <td scope={this.scope} className={this.className}>
        {children}
      </td>
    );
  }
}

function defaultCellContents<Row>(this: Column<Row>, row: Row) {
  const value = (row as any)[this.slug];

  if (typeof value === "undefined" || value === null) {
    return "";
  }

  return <>{"" + value}</>;
}

function defaultHeaderElement<Row>(this: Column<Row>, children?: ReactNode) {
  return (
    <th key={this.slug} scope="col" className={this.className}>
      {children}
    </th>
  );
}

function defaultHeaderContents<Row>(this: Column<Row>) {
  return this.title;
}

/// A drag-to-order version of DataTable.
/// NOTE: If you pass in any of the function arguments (such as getCellElement),
/// the parent component needs to be a client component as well.
/// You can't pass functions (other than Server Actions) over the client–server boundary.
export function ReorderableDataTable<Row>(props: DataTableProps<Row>) {
  const dragControls = useDragControls();
  const {
    rows,
    getTotalMessage,
    children,
    onReorderRows,
    keyColumn,
    messages: t,
  } = props;
  const columns: Column<Row>[] = props.columns.map((column) => ({
    getCellElement: column.getCellElement ?? defaultCellElement,
    getCellContents: column.getCellContents ?? defaultCellContents,
    getHeaderElement: column.getHeaderElement ?? defaultHeaderElement,
    getHeaderContents: column.getHeaderContents ?? defaultHeaderContents,
    className: "align-middle",
    ...column,
  }));

  columns.unshift({
    slug: "dragHandle",
    title: t.dragToReorder,
    getHeaderContents: () => (
      <span className="visually-hidden">{t.dragToReorder}</span>
    ),
    getHeaderElement: defaultHeaderElement,
    getCellContents: () => (
      <span title={t.dragToReorder} aria-label={t.dragToReorder}>
        ⠿
      </span>
    ),
    getCellElement(row, children) {
      // TODO: We'd probably like to disable dragging on the rest of the row,
      // leaving only dragHandle as draggable.
      // However, setting dragListener={false} on Reorder.Item causes only the first row
      // to be draggable. Trying to drag any other row will cause the first row to move.
      // The current state is "good enough" as in we provide a visual cue that we're
      // draggable, but it would be better to only allow dragging at the handle.
      return (
        <td
          className="align-middle ps-3"
          scope="row"
          onPointerDown={(e) => dragControls.start(e)}
          style={{
            cursor: "grab",
            userSelect: "none",
          }}
        >
          {children}
        </td>
      );
    },
  });

  const totalMessage = getTotalMessage?.(props.rows.length);
  const className = props.className ?? "table table-striped";

  return (
    <>
      <table className={className}>
        <thead>
          <tr>
            {columns.map((column) => (
              <Fragment key={column.slug}>
                {column.getHeaderElement!(column!.getHeaderContents!())}
              </Fragment>
            ))}
          </tr>
        </thead>
        <Reorder.Group
          as={"tbody"}
          onReorder={onReorderRows}
          values={rows}
          dragControls={dragControls}
        >
          {rows.map((row) => (
            <Reorder.Item
              as={"tr"}
              key={"" + row[keyColumn]}
              value={row}
              // dragListener={false} // TODO Bug in Motion.Reorder? See dragHandle column above
              dragControls={dragControls}
            >
              {columns.map((column) => (
                <Fragment key={column.slug}>
                  {column.getCellElement!(row, column.getCellContents!(row))}
                </Fragment>
              ))}
            </Reorder.Item>
          ))}
        </Reorder.Group>
        {children}
      </table>
      {totalMessage && <p>{totalMessage}</p>}
    </>
  );
}
