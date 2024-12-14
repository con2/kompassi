import Link from "next/link";

import { graphql } from "@/__generated__";
import {
  AdminOrderPaymentStampFragment,
  AdminOrderReceiptFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import Section from "@/components/Section";
import SignInRequired from "@/components/SignInRequired";
import ContactForm from "@/components/tickets/ContactForm";
import ProductsTable from "@/components/tickets/ProductsTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

graphql(`
  fragment AdminOrderPaymentStamp on LimitedPaymentStampType {
    createdAt
    correlationId
    provider
    type
    status
  }
`);

graphql(`
  fragment AdminOrderReceipt on LimitedReceiptType {
    correlationId
    createdAt
    email
    type
    status
  }
`);

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
          paymentStamps {
            ...AdminOrderPaymentStamp
          }
          receipts {
            ...AdminOrderReceipt
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
  const sTamp = translations.Tickets.PaymentStamp;
  const receipT = translations.Tickets.Receipt;
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

  const paymentStampColumns: Column<AdminOrderPaymentStampFragment>[] = [
    {
      slug: "createdAt",
      title: sTamp.attributes.createdAt,
      getCellContents: (stamp) => (
        <FormattedDateTime
          value={stamp.createdAt}
          locale={locale}
          scope={event}
          session={session}
        />
      ),
      className: "col-2",
    },
    {
      slug: "correlationId",
      title: sTamp.attributes.correlationId,
      className: "col-3",
    },
    {
      slug: "type",
      title: sTamp.attributes.type.title,
      getCellContents: (stamp) => sTamp.attributes.type.choices[stamp.type],
      className: "col-2",
    },
    {
      slug: "status",
      title: t.attributes.status.title,
      getCellContents: (stamp) =>
        t.attributes.status.choices[stamp.status].shortTitle,
      className: "col-2",
    },
    {
      slug: "provider",
      title: t.attributes.provider.title,
      getCellContents: (stamp) => t.attributes.provider.choices[stamp.provider],
      className: "col-3",
    },
  ];

  const receiptColumns: Column<AdminOrderReceiptFragment>[] = [
    {
      slug: "createdAt",
      title: sTamp.attributes.createdAt,
      getCellContents: (receipt) => (
        <FormattedDateTime
          value={receipt.createdAt}
          locale={locale}
          scope={event}
          session={session}
        />
      ),
      className: "col-2",
    },
    {
      slug: "correlationId",
      title: sTamp.attributes.correlationId,
      className: "col-3",
    },
    {
      slug: "type",
      title: receipT.attributes.type.title,
      getCellContents: (receipt) =>
        receipT.attributes.type.choices[receipt.type],
      className: "col-2",
    },
    {
      slug: "status",
      title: receipT.attributes.status.title,
      getCellContents: (receipt) =>
        receipT.attributes.status.choices[receipt.status],
      className: "col-2",
    },
    {
      slug: "email",
      title: t.attributes.email.title,
      className: "col-3",
    },
  ];

  const event = data.event;
  const order = data.event.tickets.order;
  const { shortTitle: paymentStatus } =
    t.attributes.status.choices[order.status];

  return (
    <ViewContainer>
      <ViewHeading>
        {t.singleTitle(order.formattedOrderNumber)}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <Section title={paymentStatus}>
        <ProductsTable
          order={order}
          messages={translations.Tickets}
          className="mb-4"
        />
      </Section>

      <Section title={t.contactForm.title}>
        <ContactForm messages={translations} values={order} isAdmin />
      </Section>

      <Section title={t.attributes.paymentStamps.title}>
        <DataTable columns={paymentStampColumns} rows={order.paymentStamps} />
      </Section>

      <Section title={t.attributes.receipts.title}>
        <DataTable columns={receiptColumns} rows={order.receipts} />
      </Section>
    </ViewContainer>
  );
}
