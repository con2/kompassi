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
  messages: Translations["Tickets"]["productsTable"];
}

export default function ProductsTable({ order, messages: t }: Props) {
  return (
    <table className="table table-striped mt-4 mb-5">
      <thead>
        <tr className="row">
          <th className="col-8">{t.product}</th>
          <th className="col text-end">{t.quantity.title}</th>
          <th className="col text-end">{t.unitPrice}</th>
        </tr>
      </thead>
      <tbody>
        {order.products.map((product, idx) => (
          <tr key={idx} className="row">
            <td className="col-8">
              <strong>{product.title}</strong>
            </td>
            <td className="col text-end">
              <span className="fs-3">
                {product.quantity}&nbsp;{t.quantity.unit}
              </span>
            </td>
            <td className="col fs-4 text-end">{formatMoney(product.price)}</td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr className="row">
          <td className="col-8">
            <strong>{t.total}</strong>
          </td>
          <td className="col text-end"></td>
          <td className="col fs-4 text-end">
            <strong>{formatMoney(order.totalPrice)}</strong>
          </td>
        </tr>
      </tfoot>
    </table>
  );
}
