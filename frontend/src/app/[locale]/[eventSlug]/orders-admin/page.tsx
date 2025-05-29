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
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
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
  query OrderList(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $searchTerm: String
  ) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        products {
          ...ProductChoice
        }

        orders(filters: $filters, search: $searchTerm) {
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
        .filter(([slug]) => slug !== PaymentStatus.NotStarted)
        .map(([slug, { shortTitle }]) => ({
          slug: slug.toLowerCase(),
          title: shortTitle,
        })),
    },
    {
      slug: "product",
      title: producT.clientAttributes.product,
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

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const filters = buildDimensionFilters(searchParams);
  const searchTerm = searchParams.search ?? "";
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, filters, searchTerm },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const orders = data.event.tickets.orders;
  const products = data.event.tickets.products;

  const dimensions = getDimensions(translations.Tickets, products);
  const queryString = new URLSearchParams(searchParams).toString();

  const columns: Column<OrderListFragment>[] = [
    {
      slug: "orderNumber",
      title: t.attributes.orderNumberAbbr,
      className: "col-1",
      getCellContents: (order) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/orders-admin/${order.id}${
            queryString ? `?${queryString}` : ""
          }`}
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
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Tickets.admin.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <a href={`/${eventSlug}/tickets`} className="btn btn-outline-primary">
            {t.actions.newOrder}…
          </a>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="orders"
        translations={translations}
        queryString={queryString}
      />

      <DimensionFilters
        dimensions={dimensions}
        className="row row-cols-md-auto g-3 align-items-center mt-1 mb-2"
        messages={{
          searchPlaceholder: t.actions.search,
        }}
        search
      />

      <DataTable rows={orders} columns={columns} />
    </ViewContainer>
  );
}
