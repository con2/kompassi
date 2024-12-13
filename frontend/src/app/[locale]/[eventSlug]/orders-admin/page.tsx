import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import {
  OrderListFragment,
  PaymentStatus,
  ProductChoiceFragment,
  QuotaListFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import { Dimension } from "@/components/dimensions/models";
import FormattedDateTime from "@/components/FormattedDateTime";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Translations } from "@/translations/en";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment OrderList on FullOrderType {
    id
    formattedOrderNumber
    displayName
    email
    createdAt
    totalPrice
    status
  }
`);

graphql(`
  fragment ProductChoice on FullProductType {
    id
    title
  }
`);

const query = graphql(`
  query OrderList($eventSlug: String!, $filters: [DimensionFilterInput!]) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        products {
          ...ProductChoice
        }

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
  searchParams: Record<string, string>;
}

function getDimensions(
  messages: Translations["Tickets"],
  products: ProductChoiceFragment[],
): Dimension[] {
  const t = messages.Order;
  const producT = messages.Product;

  return [
    {
      slug: "status",
      title: t.attributes.status.title,
      values: Object.entries(t.attributes.status.choices)
        .filter(([slug, _]) => slug != "UNKNOWN")
        .map(([slug, { shortTitle }]) => ({ slug, title: shortTitle })),
    },
    {
      slug: "product",
      title: producT.attributes.product,
      values: products.map(({ id, title }) => ({ slug: id, title })),
    },
  ];
}

export async function generateMetadata({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, filters },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    viewTitle: t.listTitle,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function OrdersPage({ params, searchParams }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const producT = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const filters = buildDimensionFilters(searchParams);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, filters },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const orders = data.event.tickets.orders;
  const products = data.event.tickets.products;

  const dimensions = getDimensions(translations.Tickets, products);

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
      slug: "email",
      title: t.attributes.email.title,
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

      <DimensionFilters
        dimensions={dimensions}
        className="row row-cols-md-auto g-3 align-items-center mt-1 mb-2"
      />

      <DataTable rows={orders} columns={columns} />
    </ViewContainer>
  );
}
