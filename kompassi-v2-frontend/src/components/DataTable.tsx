import { ReactNode, Fragment } from "react";

type Responsive = "sm" | "md" | "lg" | "xl" | boolean;

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

function ResponsiveWrapper({
  responsive,
  children,
}: {
  responsive?: Responsive;
  children?: ReactNode;
}) {
  switch (responsive) {
    case "sm":
    case "md":
    case "lg":
    case "xl":
      return <div className={`table-responsive-${responsive}`}>{children}</div>;
    case true:
      return <div className="table-responsive">{children}</div>;
    default:
      return <>{children}</>;
  }
}

interface DataTableProps<Row> {
  className?: string;
  rows: Row[];
  columns: Column<Row>[];
  getTotalMessage?: (total: number) => ReactNode;
  responsive?: Responsive;
  children?: ReactNode;
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

export function DataTable<Row>(props: DataTableProps<Row>) {
  const { rows, getTotalMessage, responsive, children } = props;
  const columns: Column<Row>[] = props.columns.map((column, index) => ({
    getCellElement: column.getCellElement ?? defaultCellElement,
    getCellContents: column.getCellContents ?? defaultCellContents,
    getHeaderElement: column.getHeaderElement ?? defaultHeaderElement,
    getHeaderContents: column.getHeaderContents ?? defaultHeaderContents,
    className: "align-middle",
    ...column,
  }));

  const totalMessage = getTotalMessage?.(props.rows.length);
  const className = props.className ?? "table table-striped";

  return (
    <ResponsiveWrapper responsive={responsive}>
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
    </ResponsiveWrapper>
  );
}
