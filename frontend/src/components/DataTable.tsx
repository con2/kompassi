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
  rows: Row[];
  columns: Column<Row>[];
  getTotalMessage?: (total: number) => ReactNode;

  /// By default, first column (0) is designated scope="row". Set to -1 to disable.
  rowScopeColumnIndex?: number;
  children?: ReactNode;
}

function defaultCellElement<Row>(
  this: Column<Row>,
  _row: Row,
  children?: ReactNode,
) {
  return (
    <td scope={this.scope} className={this.className}>
      {children}
    </td>
  );
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

export function DataTable<Row>(props: DataTableProps<Row>) {
  const { rowScopeColumnIndex } = props;
  const { rows, getTotalMessage, children } = props;
  const columns: Column<Row>[] = props.columns.map((column, index) => ({
    getCellElement: column.getCellElement ?? defaultCellElement,
    getCellContents: column.getCellContents ?? defaultCellContents,
    getHeaderElement: column.getHeaderElement ?? defaultHeaderElement,
    getHeaderContents: column.getHeaderContents ?? defaultHeaderContents,
    scope: rowScopeColumnIndex === index ? "row" : undefined,
    className: "align-middle",
    ...column,
  }));

  const totalMessage = getTotalMessage?.(props.rows.length);

  return (
    <>
      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            {columns.map((column) => (
              <Fragment key={column.slug}>
                {column.getHeaderElement!(column!.getHeaderContents!())}
              </Fragment>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map((column) => (
                <Fragment key={column.slug}>
                  {column.getCellElement!(row, column.getCellContents!(row))}
                </Fragment>
              ))}
            </tr>
          ))}
        </tbody>
        {children}
      </table>
      {totalMessage && <p>{totalMessage}</p>}
    </>
  );
}
