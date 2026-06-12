import Link from "next/link";
import { ReactNode } from "react";

import { PaymentStatus } from "@/__generated__/graphql";
import Messages from "@/components/errors/Messages";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import type { GetOrderResponse } from "@/services/tickets";
import type { Translations } from "@/translations/en";

interface Props {
  title: string;
  eventSlug: string;
  orderId: string;
  data: GetOrderResponse;
  messages: Translations["Tickets"]["Order"];
  searchParams: Record<string, string>;
  /// Rendered when the order can be cancelled in self-service.
  children: ReactNode;
}

/// Common scaffolding for the order cancellation pages (request and confirm).
/// When the order cannot be cancelled in self-service, renders guidance
/// instead of the children.
/// NOTE: These pages can be accessed without authentication (ie. we don't know
/// the accessor is the person who ordered) so absolutely no PII. In particular,
/// the email address of the order must not be shown.
export default function OrderCancellationView({
  title,
  eventSlug,
  orderId,
  data,
  messages: t,
  searchParams,
  children,
}: Props) {
  const { order, event, seller } = data;

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
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
        children
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
