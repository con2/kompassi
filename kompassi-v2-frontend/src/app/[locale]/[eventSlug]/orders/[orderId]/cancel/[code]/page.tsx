import { confirmOrderCancellation } from "../actions";
import SubmitButton from "@/components/forms/SubmitButton";
import OrderCancellationView from "@/components/tickets/OrderCancellationView";
import { getOrder } from "@/services/tickets";
import { getTranslations } from "@/translations";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    orderId: string;
    code: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

/// Order cancellation confirmation page, reached via the link in the confirmation
/// email. See OrderCancellationView for PII concerns.
export default async function OrderCancellationConfirmationPage(props: Props) {
  const { locale, eventSlug, orderId, code } = await props.params;
  const searchParams = await props.searchParams;
  const data = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const confirmT = t.cancelPage.confirm;

  return (
    <OrderCancellationView
      title={confirmT.title}
      eventSlug={eventSlug}
      orderId={orderId}
      data={data}
      messages={t}
      searchParams={searchParams}
    >
      {confirmT.warning}

      <form
        action={confirmOrderCancellation.bind(
          null,
          locale,
          eventSlug,
          orderId,
          code,
        )}
      >
        <div className="d-grid gap-2 mb-4">
          <SubmitButton className="btn btn-danger btn-lg">
            {confirmT.actions.cancelOrder}
          </SubmitButton>
        </div>
      </form>
    </OrderCancellationView>
  );
}
