import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import {
  DimensionFilterFragment,
  OrderListFragment,
  PaymentStatus,
  ProductChoiceFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { DimensionFilters } from "@/components/dimensions/DimensionFilters";
import { buildDimensionFilters } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import { decodeBoolean } from "@/helpers/decodeBoolean";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Translations } from "@/translations/en";
import { Alert } from "react-bootstrap";

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
  query AdminOrderListWithOrders(
    $eventSlug: String!
    $filters: [DimensionFilterInput!]
    $search: String
    $returnNone: Boolean = false
  ) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        products {
          ...ProductChoice
        }

        orders(filters: $filters, search: $search, returnNone: $returnNone) {
          ...OrderList
        }

        countTotalOrders
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

function getDimensions(
  messages: Translations["Tickets"],
  products: ProductChoiceFragment[],
): DimensionFilterFragment[] {
  const t = messages.Order;
  const producT = messages.Product;

  return [
    {
      slug: "status",
      title: t.attributes.status.title,
      isMultiValue: false,
      isListFilter: true,
      isKeyDimension: true,
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
      isMultiValue: false,
      isListFilter: true,
      isKeyDimension: true,
      values: products.map(({ id, title }) => ({ slug: "" + id, title })),
    },
  ];
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, returnNone: true },
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

export default async function OrdersPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  // XXX there should be a better way to handle this
  const {
    success: _success, // eslint-disable-line @typescript-eslint/no-unused-vars
    error: _error, // eslint-disable-line @typescript-eslint/no-unused-vars
    search,
    force = "false",
    ...filterSearchParams
  } = searchParams;
  const filters = buildDimensionFilters(filterSearchParams);
  const passedSearchParams = Object.fromEntries(
    Object.entries({ ...filterSearchParams, search, force }).filter(
      ([, value]) => !!value,
    ),
  );

  const showResults =
    decodeBoolean(force) || Object.entries(filters).length > 0 || !!search;
  const { data } = await getClient().query({
    query,
    variables: {
      eventSlug,
      filters,
      search,
      returnNone: !showResults,
    },
  });

  if (!data.event?.tickets) {
    notFound();
  }

  const event = data.event;
  const orders = data.event.tickets.orders;
  const products = data.event.tickets.products;
  const countTotalOrders = data.event.tickets.countTotalOrders;

  const dimensions = getDimensions(translations.Tickets, products);
  const queryString = new URLSearchParams(passedSearchParams).toString();

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

  function ForceLink({ children }: { children: React.ReactNode }) {
    const strongWithTheForce = new URLSearchParams({
      ...passedSearchParams,
      force: "strong",
    }).toString();
    return (
      <Link
        href={`/${event.slug}/orders-admin?${strongWithTheForce}`}
        className="link-subtle"
        prefetch={false}
      >
        {children}
      </Link>
    );
  }

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      searchParams={searchParams}
      active="orders"
      actions={
        <Link
          href={`/${eventSlug}/orders-admin/new`}
          className="btn btn-outline-primary"
        >
          {t.actions.newOrder.label}…
        </Link>
      }
    >
      <DimensionFilters
        dimensions={dimensions}
        messages={{
          searchPlaceholder: t.actions.search,
        }}
        search
      />

      {showResults ? (
        <DataTable rows={orders} columns={columns}>
          <tfoot>
            <tr>
              <td colSpan={columns.length}>
                <strong>
                  {t.showingOrders(orders.length, countTotalOrders)}
                </strong>
              </td>
            </tr>
          </tfoot>
        </DataTable>
      ) : (
        <Alert variant="warning">
          {t.noFiltersApplied(ForceLink, countTotalOrders)}
        </Alert>
      )}
    </TicketsAdminView>
  );
}
