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
}

export default function ProductsTable({
  order,
  messages: t,
  className,
}: Props) {
  const columns: Column<Product>[] = [
    {
      slug: "product",
      title: t.Product.attributes.product,
      getCellContents: (row) => <strong>{row.title}</strong>,
      className: "col-8",
    },
    {
      slug: "quantity",
      title: t.Product.attributes.quantity.title,
      getCellContents: (row) => (
        <>
          {row.quantity}&nbsp;{t.Product.attributes.quantity.unit}
        </>
      ),
      getHeaderElement: (children) => <th className="text-end">{children}</th>,
      className: "text-end fs-3",
    },
    {
      slug: "price",
      title: t.Product.attributes.unitPrice,
      getCellContents: (row) => <>{formatMoney(row.price)}</>,
      getHeaderElement: (children) => <th className="text-end">{children}</th>,
      className: "text-end fs-3",
    },
  ];

  className = "table table-striped " + (className ?? "");

  return (
    <DataTable className={className} rows={order.products} columns={columns}>
      <tfoot>
        <tr>
          <td className="col-8">
            <strong>{t.Order.attributes.totalPrice}</strong>
          </td>
          <td className="col text-end"></td>
          <td className="col fs-4 text-end">
            <strong>{formatMoney(order.totalPrice)}</strong>
          </td>
        </tr>
      </tfoot>
    </DataTable>
  );
}
