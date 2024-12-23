import { Temporal } from "@js-temporal/polyfill";
import Link from "next/link";
import { notFound } from "next/navigation";

import { createProduct } from "./actions";
import { graphql } from "@/__generated__";
import { ProductListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment ProductList on FullProductType {
    id
    title
    description
    price
    isAvailable
    availableFrom
    availableUntil
    countPaid
    countReserved
    countAvailable
  }
`);

const query = graphql(`
  query ProductList($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        products {
          ...ProductList
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

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Tickets.Product;

  // while dimension filters are not needed to form the title,
  // we would like to do only one query per request
  // so do the exact same query here so that it can be cached
  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
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

export default async function ProductsPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Product;
  const session = await auth();

  // TODO encap
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
  const products = data.event.tickets.products;

  const newProductFields: Field[] = [
    {
      slug: "title",
      title: t.attributes.title,
      type: "SingleLineText",
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows: 3,
      ...t.attributes.description,
    },
    {
      slug: "price",
      type: "DecimalField",
      decimalPlaces: 2,
      ...t.attributes.unitPrice,
    },
  ];

  const columns: Column<ProductListFragment>[] = [
    {
      slug: "title",
      title: t.attributes.product,
      getCellContents: (product) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/products/${product.id}`}
        >
          {product.title}
        </Link>
      ),
    },
    {
      slug: "availability",
      title: t.attributes.isAvailable.title,
      getCellContents: (product) => {
        let activityEmoji = product.isAvailable ? "✅" : "❌";
        let message = "";

        // TODO(#436) proper handling of event & session time zones
        // Change untilTime(t: String): String to UntilTime(props: { children: ReactNode }): ReactNode
        // and init as <….UntilTime><FormattedDateTime … /></UntilTime>?
        if (product.isAvailable) {
          if (product.availableUntil) {
            message = t.attributes.isAvailable.untilTime(
              formatDateTime(product.availableUntil, locale),
            );
          } else {
            message = t.attributes.isAvailable.untilFurtherNotice;
          }
        } else {
          if (
            product.availableFrom &&
            Temporal.Instant.compare(
              Temporal.Instant.from(product.availableFrom),
              Temporal.Now.instant(),
            ) > 0
          ) {
            activityEmoji = "⏳";
            message = t.attributes.isAvailable.openingAt(
              formatDateTime(product.availableFrom, locale),
            );
          } else {
            message = t.attributes.isAvailable.notAvailable;
          }
        }

        return `${activityEmoji} ${message}`;
      },
    },
    {
      slug: "countPaid",
      title: t.attributes.countPaid,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countReserved",
      title: t.attributes.countReserved.title,
      getHeaderContents: () => (
        <abbr title={t.attributes.countReserved.description}>
          {t.attributes.countReserved.title}
        </abbr>
      ),
      className: "text-end align-middle col-1",
    },
    {
      slug: "countAvailable",
      title: t.attributes.countAvailable,
      className: "text-end align-middle col-1",
    },
    {
      slug: "price",
      title: t.attributes.unitPrice.title,
      getCellContents: (product) => formatMoney(product.price),
      className: "text-end align-middle col-2",
    },
  ];

  // TODO let the backend calculate these with decimals
  const totalReserved = formatMoney(
    "" +
      products.reduce(
        (acc, product) =>
          acc + product.countReserved * parseFloat(product.price),
        0,
      ),
  );
  const totalPaid = formatMoney(
    "" +
      products.reduce(
        (acc, product) => acc + product.countPaid * parseFloat(product.price),
        0,
      ),
  );

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Tickets.admin.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.newProduct.title}
            messages={t.actions.newProduct.modalActions}
            action={createProduct.bind(null, locale, eventSlug)}
            className="btn btn-outline-primary"
          >
            <SchemaForm
              fields={newProductFields}
              messages={translations.SchemaForm}
            />
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="products"
        translations={translations}
      />

      <DataTable rows={products} columns={columns}>
        <tfoot>
          <tr>
            <th colSpan={5} className="text-end align-middle" scope="row">
              {t.attributes.totalPaid}
            </th>
            <th className="text-end align-middle col-2">{totalPaid}</th>
          </tr>
          <tr>
            <th colSpan={5} className="text-end align-middle" scope="row">
              <abbr title={t.attributes.countReserved.description}>
                {t.attributes.totalReserved}
              </abbr>
            </th>
            <th className="text-end align-middle col-2">{totalReserved}</th>
          </tr>
        </tfoot>
      </DataTable>
    </ViewContainer>
  );
}
