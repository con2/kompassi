import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { OrderListFragment, QuotaListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment OrderList on FullOrderType {
    id
    formattedOrderNumber
    displayName
    createdAt
    totalPrice
    status
  }
`);

const query = graphql(`
  query OrderList($eventSlug: String!, $filters: [DimensionFilterInput!]) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        orders(filters: $filters) {
          ...OrderList
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: t.Order.listTitle,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function OrdersPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const producT = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const orders = data.event.tickets.orders;

  const columns: Column<OrderListFragment>[] = [
    {
      slug: "orderNumber",
      title: t.attributes.orderNumber,
      className: "col-1",
      getCellContents: (order) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/orders-admin/${order.id}`}
        >
          {order.formattedOrderNumber}
        </Link>
      ),
    },
    {
      slug: "displayName",
      title: t.attributes.displayName.title,
    },
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (order) => (
        <FormattedDateTime
          value={order.createdAt}
          locale={locale}
          scope={event}
          session={session}
        />
      ),
    },
    {
      slug: "status",
      title: t.attributes.status.title,
      getCellContents: (order) =>
        t.attributes.status.choices[order.status].shortTitle,
    },
    {
      slug: "totalPrice",
      title: t.attributes.totalPrice,
      getCellContents: (order) => formatMoney(order.totalPrice),
      className: "text-end col-2",
    },
  ];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.listTitle}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="orders"
        translations={translations}
      />

      <DataTable rows={orders} columns={columns} />
    </ViewContainer>
  );
}
