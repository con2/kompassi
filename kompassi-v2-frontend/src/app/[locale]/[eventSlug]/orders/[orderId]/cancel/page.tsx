import Link from "next/link";

import { requestOrderCancellation } from "./actions";
import { PaymentStatus } from "@/__generated__/graphql";
import Messages from "@/components/errors/Messages";
import FormattedDateTime from "@/components/FormattedDateTime";
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
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

/// NOTE: This page can be accessed without authentication (ie. we don't know the accessor
/// is the person who ordered) so absolutely no PII. In particular, the email address of
/// the order must not be shown.
export default async function OrderCancellationPage(props: Props) {
  const { locale, eventSlug, orderId } = await props.params;
  const searchParams = await props.searchParams;
  const { order, event, seller } = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const cancelT = t.cancelPage;

  return (
    <ViewContainer>
      <ViewHeading>
        {cancelT.title}
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
          {cancelT.explanation}

          {order.cancellationDeadline && (
            <p>
              {cancelT.deadline(
                <FormattedDateTime
                  value={order.cancellationDeadline}
                  locale={locale}
                  scope={undefined}
                  session={undefined}
                />,
              )}
            </p>
          )}

          <form
            action={requestOrderCancellation.bind(
              null,
              locale,
              eventSlug,
              orderId,
            )}
          >
            <div className="d-grid gap-2 mb-4">
              <SubmitButton className="btn btn-danger btn-lg">
                {cancelT.actions.sendConfirmationEmail}
              </SubmitButton>
            </div>
          </form>
        </>
      ) : order.status === PaymentStatus.Paid ? (
        <p>{t.actions.requestCancellation.contactTicketSales(seller.email)}</p>
      ) : (
        <p>{cancelT.notCancellable}</p>
      )}

      <Link href={`/${eventSlug}/orders/${orderId}`}>
        {cancelT.actions.returnToOrderPage}
      </Link>
    </ViewContainer>
  );
}
