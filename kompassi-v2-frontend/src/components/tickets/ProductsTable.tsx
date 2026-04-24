import { Column, DataTable } from "../DataTable";
import formatMoney from "@/helpers/formatMoney";
import formatVatRate from "@/helpers/formatVatRate";
import type { Translations } from "@/translations/en";

interface Product {
  title: string;
  quantity: number;
  price: string;
  vatPercentage: string;
}

interface Order {
  totalPrice: string;
  products: Product[];
}

interface Props {
  order: Order;
  locale: string;
  messages: Translations["Tickets"];
  className?: string;
  compact?: boolean;
}

function computeVatBreakdown(
  products: Product[],
): { rate: string; vat: string }[] {
  const totals = new Map<string, number>();
  for (const p of products) {
    const gross = parseFloat(p.price) * p.quantity;
    const prev = totals.get(p.vatPercentage) ?? 0;
    totals.set(p.vatPercentage, prev + gross);
  }
  return Array.from(totals.entries())
    .sort(([a], [b]) => parseFloat(a) - parseFloat(b))
    .map(([rate, gross]) => {
      const r = parseFloat(rate);
      const vat = (gross * r) / (100 + r);
      return { rate, vat: vat.toFixed(2) };
    });
}

export default function ProductsTable({
  order,
  locale,
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

  const vatBreakdown = computeVatBreakdown(order.products);

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
        {vatBreakdown.map(({ rate, vat }) => (
          <tr key={rate} className="text-muted">
            <td className="col-8 small">
              {t.Product.clientAttributes.vatIncluded(
                formatVatRate(rate, locale),
              )}
            </td>
            <td className="col text-end"></td>
            <td className="col text-end small">{formatMoney(vat)}</td>
          </tr>
        ))}
      </tfoot>
    </DataTable>
  );
}
