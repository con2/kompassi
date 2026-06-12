import Link from "next/link";
import { ReactNode } from "react";

import { payOrder } from "./actions";
import { PaymentStatus } from "@/__generated__/graphql";
import Messages from "@/components/errors/Messages";
import Section from "@/components/Section";
import OrderHeader from "@/components/tickets/OrderHeader";
import ProductsTable from "@/components/tickets/ProductsTable";
import RequestCancellationSection from "@/components/tickets/RequestCancellationSection";
import SellerSection from "@/components/tickets/SellerSection";
import ViewContainer from "@/components/ViewContainer";
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

/// NOTE: This page is on the Critical Path of the Hunger Games, so be extra mindful of performance.
/// Also this page can be accessed without authentication (ie. we don't know the accessor is the person who ordered)
/// so absolutely no PII.
export default async function OrderPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale, eventSlug, orderId } = params;
  const { order, event, seller } = await getOrder(eventSlug, orderId);
  const translations = getTranslations(locale);
  const t = translations.Tickets;

  function ProfileLink({ children }: { children: ReactNode }) {
    return <Link href={`/profile/orders`}>{children}</Link>;
  }

  const showPayButton =
    order.status === PaymentStatus.NotStarted ||
    order.status === PaymentStatus.Failed ||
    order.status === PaymentStatus.Pending;

  const showProfileMessage =
    order.status === PaymentStatus.NotStarted ||
    order.status === PaymentStatus.Pending ||
    order.status === PaymentStatus.Failed ||
    order.status === PaymentStatus.Paid;

  return (
    <ViewContainer>
      <OrderHeader order={order} messages={t} locale={locale} event={event} />

      <Messages messages={t.Order.cancelMessages} searchParams={searchParams} />

      <ProductsTable order={order} locale={locale} messages={t} />

      <SellerSection seller={seller} messages={t.Order.attributes.seller} />

      {showPayButton && (
        <Section>
          <form action={payOrder.bind(null, locale, eventSlug, orderId)}>
            <div className="d-grid gap-2">
              <button className="btn btn-primary btn-lg" type="submit">
                {t.Order.actions.pay}
              </button>
            </div>
          </form>
        </Section>
      )}

      <RequestCancellationSection
        order={order}
        cancelHref={`/${eventSlug}/orders/${orderId}/cancel`}
        contactEmail={seller.email}
        messages={t.Order.actions.requestCancellation}
      />

      {showProfileMessage && <p>{t.Order.profileMessage(ProfileLink)}</p>}
    </ViewContainer>
  );
}
