import Link from "next/link";

import { graphql } from "@/__generated__";
import { PaymentStatus } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/SignInRequired";
import ProductsTable from "@/components/tickets/ProductsTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query AdminOrderDetail($eventSlug: String!, $orderId: String!) {
    event(slug: $eventSlug) {
      slug
      name

      tickets {
        order(id: $orderId) {
          id
          formattedOrderNumber
          createdAt
          totalPrice
          status
          electronicTicketsLink
          firstName
          lastName
          email
          phone
          products {
            title
            quantity
            price
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    orderId: string;
  };
}

export const revalidate = 0;

export default async function ProfileOrderPage({ params }: Props) {
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
  if (!data.event?.tickets?.order) {
    const error = t.errors.ORDER_NOT_FOUND;
    return (
      <ViewContainer>
        <ViewHeading>{error.title}</ViewHeading>
        <p>{error.message}</p>
        <Link className="btn btn-primary" href={`/${eventSlug}/orders-admin`}>
          {error.actions.returnToOrderList}
        </Link>
      </ViewContainer>
    );
  }

  const event = data.event;
  const order = data.event.tickets.order;
  const { title, message } = t.attributes.status.choices[order.status];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.singleTitle(order.formattedOrderNumber)}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <h2 className="mt-4">{title}</h2>

      <ProductsTable order={order} messages={translations.Tickets} />

      {order.status == PaymentStatus.Pending && order.electronicTicketsLink && (
        <div className="d-grid gap-2 mb-4">
          <Link className="btn btn-primary" href={order.electronicTicketsLink}>
            {t.actions.downloadTickets.title}
          </Link>
        </div>
      )}
    </ViewContainer>
  );
}
