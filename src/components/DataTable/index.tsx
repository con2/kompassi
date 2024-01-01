import { ReactNode } from "react";

export interface Column<Row> {
  slug: string;
  title: string;
  getCell?: (row: Row) => ReactNode;
}

interface DataTableProps<Row> {
  rows: Row[];
  columns: Column<Row>[];
  getTotalMessage?: (total: number) => ReactNode;

  /// By default, first column (0) is designated scope="row". Set to -1 to disable.
  rowScopeColumnIndex?: number;
}

function defaultCellGetter<Row>(this: Column<Row>, row: Row) {
  const value = (row as any)[this.slug];

  if (typeof value === "undefined" || value === null) {
    return "";
  }

  return "" + value;
}

export function DataTable<Row>(props: DataTableProps<Row>) {
  const columns = props.columns.map((column) => ({
    getCell: column.getCell || defaultCellGetter,
    ...column,
  }));

  const totalMessage = props.getTotalMessage?.(props.rows.length);
  const rowScopeColumnIndex = props.rowScopeColumnIndex ?? 0;

  return (
    <>
      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.slug} scope="col" className="align-middle">
                {column.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {props.rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map((column) => (
                <td
                  key={column.slug}
                  scope={idx === rowScopeColumnIndex ? "row" : undefined}
                  className="align-middle"
                >
                  {column.getCell(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {totalMessage && <p>{totalMessage}</p>}
    </>
  );
}
