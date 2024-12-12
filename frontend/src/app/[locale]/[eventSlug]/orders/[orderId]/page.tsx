import { payOrder } from "./actions";
import ProductsTable from "@/components/tickets/ProductsTable";
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
  const { title, message } = t.Order.attributes.status.choices[order.status];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.Order.singleTitle(formatOrderNumber(order.orderNumber))}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <h2 className="mt-4">{title}</h2>
      <p>{message}</p>

      <ProductsTable order={order} messages={t} />

      {order.status == "PENDING" && (
        <form action={payOrder.bind(null, locale, eventSlug, orderId)}>
          <div className="d-grid gap-2 mb-4">
            <button className="btn btn-primary btn-lg" type="submit">
              {t.Order.actions.pay.title}
            </button>
          </div>
        </form>
      )}
    </ViewContainer>
  );
}
