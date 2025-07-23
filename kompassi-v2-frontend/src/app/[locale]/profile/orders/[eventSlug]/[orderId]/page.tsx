import Link from "next/link";

import { notFound } from "next/navigation";
import { payOrder } from "../../actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { cancelOrder } from "@/app/[locale]/[eventSlug]/orders/[orderId]/actions";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import ModalButton from "@/components/ModalButton";
import OrderHeader from "@/components/tickets/OrderHeader";
import ProductsTable from "@/components/tickets/ProductsTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProfileOrderDetail($eventSlug: String!, $orderId: String!) {
    profile {
      tickets {
        order(eventSlug: $eventSlug, id: $orderId) {
          id
          formattedOrderNumber
          createdAt
          totalPrice
          status
          eticketsLink
          canPay
          canCancel
          products {
            title
            quantity
            price
          }

          event {
            slug
            name
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    orderId: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, orderId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, orderId },
  });

  if (!data.profile?.tickets?.order) {
    notFound();
  }

  const order = data.profile.tickets.order;
  const paymentStatus = t.attributes.status.choices[order.status].shortTitle;
  const title = getPageTitle({
    subject: t.singleTitle(order.formattedOrderNumber, paymentStatus),
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ProfileOrderPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, orderId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, orderId },
  });
  if (!data.profile?.tickets?.order) {
    const error = t.errors.ORDER_NOT_FOUND;
    return (
      <ViewContainer>
        <ViewHeading>{error.title}</ViewHeading>
        <p>{error.message}</p>
        <Link className="btn btn-primary" href="/profile/orders">
          {error.actions.returnToOrderList}
        </Link>
      </ViewContainer>
    );
  }

  const order = data.profile.tickets.order;

  return (
    <ViewContainer>
      <OrderHeader
        order={order}
        messages={translations.Tickets}
        locale={locale}
        session={session}
        event={order.event}
      />

      <ProductsTable order={order} messages={translations.Tickets} />

      {order.canPay && (
        <form action={payOrder.bind(null, locale, eventSlug, orderId)}>
          <div className="d-grid gap-2 mb-4">
            <button className="btn btn-primary btn-lg" type="submit">
              {t.actions.pay}
            </button>
          </div>
        </form>
      )}

      {order.eticketsLink && (
        <div className="d-grid gap-2 mb-4">
          <Link className="btn btn-primary" href={order.eticketsLink}>
            {t.actions.viewTickets}
          </Link>
        </div>
      )}

      {order.canCancel && (
        <div className="d-grid gap-2 mb-4">
          <ModalButton
            className="btn btn-outline-danger"
            label={t.actions.ownerCancel.title + "…"}
            title={t.actions.ownerCancel.title}
            messages={t.actions.ownerCancel.modalActions}
            action={cancelOrder.bind(null, locale, order.event.slug, order.id)}
          >
            {t.actions.ownerCancel.message}
          </ModalButton>
        </div>
      )}
    </ViewContainer>
  );
}
