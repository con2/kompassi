import Link from "next/link";

import { graphql } from "@/__generated__";
import {
  AdminOrderPaymentStampFragment,
  AdminOrderReceiptFragment,
  PaymentStatus,
  ReceiptType,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import ModalButton from "@/components/ModalButton";
import Section from "@/components/Section";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
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
          eticketsLink
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
  searchParams: string;
}

export const revalidate = 0;

export default async function AdminOrderPage({ params, searchParams }: Props) {
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
      className: "col-2 align-middle",
    },
    {
      slug: "correlationId",
      title: sTamp.attributes.correlationId,
      className: "col-3 align-middle",
    },
    {
      slug: "type",
      title: sTamp.attributes.type.title,
      getCellContents: (stamp) => sTamp.attributes.type.choices[stamp.type],
      className: "col-2 align-middle",
    },
    {
      slug: "status",
      title: t.attributes.status.title,
      getCellContents: (stamp) =>
        t.attributes.status.choices[stamp.status].shortTitle,
      className: "col-2 align-middle",
    },
    {
      slug: "provider",
      title: t.attributes.provider.title,
      getCellContents: (stamp) => t.attributes.provider.choices[stamp.provider],
      className: "col-2 align-middle",
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      className: "col-1 align-middle",
      getCellContents: (stamp) => (
        <>
          {stamp.status == PaymentStatus.Paid && (
            <ModalButton
              title="Refund"
              className="btn btn-sm btn-danger"
              submitButtonVariant="danger"
              messages={{
                submit: "Refund",
                cancel: "Close without refunding",
              }}
            >
              <p>This will</p>
              <ol>
                <li>mark the order as cancelled,</li>
                <li>invalidate any electronic tickets, and</li>
                <li>request the payment processor to refund the payment.</li>
              </ol>
              <p>
                <strong>NOTE:</strong> The refund may fail if there are not
                sufficient funds deposited with the payment processor. In this
                case, you need to transfer funds and complete the refund via the
                merchant panel of the payment processor.
              </p>
            </ModalButton>
          )}
        </>
      ),
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
      className: "col-2 align-middle",
    },
    {
      slug: "correlationId",
      title: sTamp.attributes.correlationId,
      className: "col-3 align-middle",
    },
    {
      slug: "type",
      title: receipT.attributes.type.title,
      getCellContents: (receipt) =>
        receipT.attributes.type.choices[receipt.type],
      className: "col-2 align-middle",
    },
    {
      slug: "status",
      title: receipT.attributes.status.title,
      getCellContents: (receipt) =>
        receipT.attributes.status.choices[receipt.status],
      className: "col-2 align-middle",
    },
    {
      slug: "email",
      title: t.attributes.email.title,
      className: "col-2 align-middle",
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      className: "col-1 align-middle",
      getCellContents: (receipt) => (
        <>
          {false && receipt.type == ReceiptType.OrderConfirmation && (
            <ModalButton
              title="Resend"
              className="btn btn-sm btn-primary"
              submitButtonVariant="primary"
              messages={{
                submit: "Resend",
                cancel: "Close without resending",
              }}
            >
              <p>
                Are you sure you want to resend the order confirmation email
                (incl. electronic tickets, if any) to the customer?
              </p>
            </ModalButton>
          )}
        </>
      ),
    },
  ];

  const event = data.event;
  const order = data.event.tickets.order;
  const { shortTitle: paymentStatus } =
    t.attributes.status.choices[order.status];

  const queryString = new URLSearchParams(searchParams).toString();
  console.log({ searchParams });

  return (
    <ViewContainer>
      <ViewHeading>
        {translations.Tickets.admin.title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="orders"
        translations={translations}
        queryString={queryString}
      />

      <Section
        title={t.singleTitle(order.formattedOrderNumber, paymentStatus)}
        className="mt-4 mb-4"
      >
        <ProductsTable order={order} messages={translations.Tickets} />
      </Section>

      <Section title={t.contactForm.title}>
        <ContactForm messages={translations} values={order} isAdmin />
      </Section>

      <Section title={sTamp.listTitle}>
        <DataTable columns={paymentStampColumns} rows={order.paymentStamps} />
      </Section>

      <Section title={receipT.listTitle}>
        <DataTable columns={receiptColumns} rows={order.receipts} />
      </Section>
    </ViewContainer>
  );
}
