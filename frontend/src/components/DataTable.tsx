import { ReactNode, Fragment } from "react";

export interface Column<Row> {
  slug: string;
  title: string;
  getCellElement?: (row: Row, children?: ReactNode) => ReactNode;
  getCellContents?: (row: Row) => ReactNode;
  scope?: string;
}

interface DataTableProps<Row> {
  rows: Row[];
  columns: Column<Row>[];
  getTotalMessage?: (total: number) => ReactNode;

  /// By default, first column (0) is designated scope="row". Set to -1 to disable.
  rowScopeColumnIndex?: number;
}

function defaultCellElement<Row>(
  this: Column<Row>,
  _row: Row,
  children?: ReactNode,
) {
  return (
    <td scope={this.scope} className="align-middle">
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

export function DataTable<Row>(props: DataTableProps<Row>) {
  const { rowScopeColumnIndex } = props;
  const columns = props.columns.map((column, index) => ({
    getCellElement: column.getCellElement ?? defaultCellElement,
    getCellContents: column.getCellContents ?? defaultCellContents,
    scope: rowScopeColumnIndex === index ? "row" : undefined,
    ...column,
  }));

  const totalMessage = props.getTotalMessage?.(props.rows.length);

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
                <Fragment key={column.slug}>
                  {column.getCellElement(row, column.getCellContents(row))}
                </Fragment>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {totalMessage && <p>{totalMessage}</p>}
    </>
  );
}
