import { Temporal } from "@js-temporal/polyfill";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { ProductListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import type { Translations } from "@/translations/en";
import { createProduct, reorderProducts } from "./actions";
import ReorderableProductsTable from "./ReorderableProductsTable";

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
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
}

export interface PreparedProduct extends ProductListFragment {
  availabilityMessage: string;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
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

// NOTE: result passed into client component
// Uses markup-returning functions from i18n
// Don't try to make a component out of this, you will regret it
export function getAvailabilityMessage(
  product: ProductListFragment,
  t: Translations["Tickets"]["Product"],
  locale: string,
) {
  let activityEmoji = product.isAvailable ? "✅" : "❌";
  let message = "";

  // TODO(#436) proper handling of event & session time zones
  // Change untilTime(t: String): String to UntilTime(props: { children: ReactNode }): ReactNode
  // and init as <….UntilTime><FormattedDateTime … /></UntilTime>?
  if (product.isAvailable) {
    if (product.availableUntil) {
      message = t.serverAttributes.isAvailable.untilTime(
        formatDateTime(product.availableUntil, locale),
      );
    } else {
      message = t.serverAttributes.isAvailable.untilFurtherNotice;
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
      message = t.serverAttributes.isAvailable.openingAt(
        formatDateTime(product.availableFrom, locale),
      );
    } else {
      message = t.serverAttributes.isAvailable.notAvailable;
    }
  }

  return `${activityEmoji} ${message}`;
}

export default async function ProductsPage(props: Props) {
  const params = await props.params;
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
      title: t.clientAttributes.title,
      required: true,
      type: "SingleLineText",
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows: 3,
      ...t.clientAttributes.description,
    },
    {
      slug: "price",
      type: "DecimalField",
      required: true,
      decimalPlaces: 2,
      ...t.clientAttributes.unitPrice,
    },
    {
      slug: "quota",
      type: "NumberField",
      ...t.clientAttributes.newProductQuota,
    },
  ];

  // Pre-render some fields for client component
  const preparedProducts: PreparedProduct[] = products.map((product) => ({
    ...product,
    availabilityMessage: getAvailabilityMessage(product, t, locale),
  }));

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      active="products"
      actions={
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
      }
    >
      <ReorderableProductsTable
        event={event}
        products={preparedProducts}
        messages={t.clientAttributes}
        onReorder={reorderProducts.bind(null, locale, eventSlug)}
      />
    </TicketsAdminView>
  );
}
