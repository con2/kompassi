import { payOrder } from "./actions";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import { getOrder } from "@/services/orders";
import { getTranslations } from "@/translations";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    orderId: string;
  };
}

export const revalidate = 0;

function formatOrderNumber(orderNumber: number) {
  return `#${orderNumber.toString().padStart(6, "0")}`;
}

/// NOTE: This page is on the Critical Path of the Hunger Games, so be extra mindful of performance.
/// Also this page can be accessed without authentication (ie. we don't know the accessor is the person who ordered)
/// so absolutely no PII.
export default async function OrderPage({ params }: Props) {
  const { locale, eventSlug, orderId } = params;
  const { order, event } = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets;
  const { title, message } = t.orderStatus[order.status];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.orderPage.title(formatOrderNumber(order.orderNumber))}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <h2 className="mt-4">{title}</h2>
      <p>{message}</p>

      <table className="table table-striped mt-4 mb-5">
        <thead>
          <tr className="row">
            <th className="col-8">{t.productsTable.product}</th>
            <th className="col text-end">{t.productsTable.quantity.title}</th>
            <th className="col text-end">{t.productsTable.unitPrice}</th>
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
                  {product.quantity}&nbsp;{t.productsTable.quantity.unit}
                </span>
              </td>
              <td className="col fs-4 text-end">
                {formatMoney(product.price)}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="row">
            <td className="col-8">
              <strong>{t.productsTable.total}</strong>
            </td>
            <td className="col text-end"></td>
            <td className="col fs-4 text-end">
              <strong>{formatMoney(order.totalPrice)}</strong>
            </td>
          </tr>
        </tfoot>
      </table>

      {order.status == "PENDING" && (
        <form action={payOrder.bind(null, locale, eventSlug, orderId)}>
          <div className="d-grid gap-2 mb-4">
            <button className="btn btn-primary btn-lg" type="submit">
              {t.orderPage.payButtonText}
            </button>
          </div>
        </form>
      )}
    </ViewContainer>
  );
}
