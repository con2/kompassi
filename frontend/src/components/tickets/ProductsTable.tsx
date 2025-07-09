import { Column, DataTable } from "../DataTable";
import formatMoney from "@/helpers/formatMoney";
import type { Translations } from "@/translations/en";

interface Product {
  title: string;
  quantity: number;
  price: string;
}

interface Order {
  totalPrice: string;
  products: Product[];
}

interface Props {
  order: Order;
  messages: Translations["Tickets"];
  className?: string;
  compact?: boolean;
}

export default function ProductsTable({
  order,
  messages: t,
  className,
  compact,
}: Props) {
  const columns: Column<Product>[] = [
    {
      slug: "product",
      title: t.Product.clientAttributes.product,
      getCellElement(_row, children) {
        return (
          <th scope="row" className={this.className}>
            {children}
          </th>
        );
      },
      getCellContents: (row) => row.title,
      className: "col-8 align-middle",
      scope: "row",
    },
    {
      slug: "quantity",
      title: t.Product.clientAttributes.quantity.title,
      getCellContents: (row) => (
        <>
          {row.quantity}&nbsp;{t.Product.clientAttributes.quantity.unit}
        </>
      ),
      getHeaderElement: (children) => <th className="text-end">{children}</th>,
      className: compact ? "text-end" : "text-end fs-3",
    },
    {
      slug: "price",
      title: t.Product.clientAttributes.unitPrice.title,
      getCellContents: (row) => <>{formatMoney(row.price)}</>,
      getHeaderElement: (children) => <th className="text-end">{children}</th>,
      className: compact ? "text-end" : "text-end fs-3",
    },
  ];

  className = "table table-striped " + (className ?? "mb-5");

  return (
    <DataTable className={className} rows={order.products} columns={columns}>
      <tfoot>
        <tr>
          <td className="col-8">
            <strong>{t.Order.attributes.totalPrice}</strong>
          </td>
          <td className="col text-end"></td>
          <td className={compact ? "col text-end" : "col text-end fs-4"}>
            <strong>{formatMoney(order.totalPrice)}</strong>
          </td>
        </tr>
      </tfoot>
    </DataTable>
  );
}
