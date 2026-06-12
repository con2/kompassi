import Link from "next/link";

import { confirmOrderCancellation } from "../actions";
import { PaymentStatus } from "@/__generated__/graphql";
import Messages from "@/components/errors/Messages";
import SubmitButton from "@/components/forms/SubmitButton";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
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

/// Order cancellation confirmation page, reached via the link in the confirmation email.
/// NOTE: This page can be accessed without authentication (ie. we don't know the accessor
/// is the person who ordered) so absolutely no PII.
export default async function OrderCancellationConfirmationPage(props: Props) {
  const { locale, eventSlug, orderId, code } = await props.params;
  const searchParams = await props.searchParams;
  const { order, event, seller } = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const confirmT = t.cancelPage.confirm;

  return (
    <ViewContainer>
      <ViewHeading>
        {confirmT.title}
        <ViewHeading.Sub>
          {t.singleTitle(
            order.formattedOrderNumber,
            t.attributes.status.choices[order.status].shortTitle,
          )}
          {", "}
          {event.name}
        </ViewHeading.Sub>
      </ViewHeading>

      <Messages messages={t.cancelMessages} searchParams={searchParams} />

      {order.canRequestCancellation ? (
        <>
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
        </>
      ) : order.status === PaymentStatus.Paid ? (
        <p>{t.actions.requestCancellation.contactTicketSales(seller.email)}</p>
      ) : (
        <p>{t.cancelPage.notCancellable}</p>
      )}

      <Link href={`/${eventSlug}/orders/${orderId}`}>
        {t.cancelPage.actions.returnToOrderPage}
      </Link>
    </ViewContainer>
  );
}
