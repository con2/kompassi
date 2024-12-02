import { getOrder } from "./service";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import { getTranslations } from "@/translations";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    orderId: string;
  };
}

export const revalidate = 1;

/// NOTE: This page is on the Critical Path of the Hunger Games, so be extra mindful of performance.
/// Also this page can be accessed without authentication (ie. we don't know the accessor is the person who ordered)
/// so absolutely no PII.
export default async function OrderPage({ params }: Props) {
  const { locale, eventSlug, orderId } = params;
  const { order, event } = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets;
  const { title, message } = t.orderState[order.status];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.orderPage.title(orderId)}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <h2 className="mt-4">{title}</h2>
      <p>{message}</p>

      <table className="table table-striped mt-4 mb-5">
        <thead>
          <tr className="row">
            <th className="col-8">{t.productsTable.product}</th>
            <th className="col">{t.productsTable.price}</th>
            <th className="col">{t.productsTable.quantity.title}</th>
          </tr>
        </thead>
        <tbody>
          {order.products.map((product, idx) => (
            <tr key={idx} className="row">
              <td className="col-8">
                <strong>{product.title}</strong>
              </td>
              <td className="col fs-4">{formatMoney(product.price)}</td>
              <td className="col">
                <span className="fs-3">
                  {product.quantity}&nbsp;{t.productsTable.quantity.unit}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="row">
            <td className="col-8">
              <strong>{t.productsTable.total}</strong>
            </td>
            <td className="col fs-4">
              <strong>{formatMoney(order.total)}</strong>
            </td>
            <td className="col"></td>
          </tr>
        </tfoot>
      </table>

      <div className="d-grid gap-2 mb-4">
        <button className="btn btn-primary btn-lg" type="submit">
          {t.orderPage.payButtonText}
        </button>
      </div>
    </ViewContainer>
  );
}
