import Link from "next/link";

import { notFound } from "next/navigation";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import {
  cancelAndRefund,
  cancelWithoutRefunding,
  resendConfirmation,
  updateOrder,
} from "./actions";
import { graphql } from "@/__generated__";
import {
  AdminOrderPaymentStampFragment,
  AdminOrderReceiptFragment,
  PaymentStatus,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ContactForm from "@/components/tickets/ContactForm";
import ProductsTable from "@/components/tickets/ProductsTable";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
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

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, orderId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, orderId },
  });

  if (!data.event?.tickets?.order) {
    notFound();
  }

  const event = data.event;
  const order = data.event.tickets.order;
  const { shortTitle: paymentStatus } =
    t.attributes.status.choices[order.status];

  const title = getPageTitle({
    event,
    subject: t.singleTitle(order.formattedOrderNumber, paymentStatus),
    translations,
  });

  return {
    title,
  };
}

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
      className: "col-3 align-middle small",
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
      className: "col-3 align-middle small",
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
  ];

  const event = data.event;
  const order = data.event.tickets.order;
  const { shortTitle: paymentStatus } =
    t.attributes.status.choices[order.status];

  const queryString = new URLSearchParams(searchParams).toString();
  const showCancelWithoutRefundingButton =
    order.status === PaymentStatus.Pending ||
    order.status === PaymentStatus.Failed ||
    order.status === PaymentStatus.Paid;

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

      <Card className="mb-4">
        <CardBody>
          <CardTitle>
            {t.singleTitle(order.formattedOrderNumber, paymentStatus)}
          </CardTitle>
          <ProductsTable
            order={order}
            messages={translations.Tickets}
            className="mb-3"
          />
          <ButtonGroup className="mt-2">
            {order.eticketsLink && (
              <a
                href={order.eticketsLink}
                target="_blank"
                rel="noopener noreferer"
                className="btn btn-primary"
              >
                {t.actions.viewTickets}…
              </a>
            )}
            {order.status === PaymentStatus.Paid && (
              <>
                <ModalButton
                  title={t.actions.resendOrderConfirmation.title}
                  className="btn btn-success"
                  submitButtonVariant="success"
                  messages={t.actions.resendOrderConfirmation.modalActions}
                  action={resendConfirmation.bind(
                    null,
                    locale,
                    eventSlug,
                    order.id,
                  )}
                >
                  <p>
                    {t.actions.resendOrderConfirmation.message(order.email)}
                  </p>
                </ModalButton>
                <ModalButton
                  title={t.actions.cancelAndRefund.title}
                  className="btn btn-danger"
                  submitButtonVariant="danger"
                  messages={t.actions.cancelAndRefund.modalActions}
                  action={cancelAndRefund.bind(
                    null,
                    locale,
                    eventSlug,
                    order.id,
                  )}
                >
                  {t.actions.cancelAndRefund.message}
                </ModalButton>
              </>
            )}
            {showCancelWithoutRefundingButton && (
              <>
                <ModalButton
                  title={t.actions.cancelWithoutRefunding.title}
                  className="btn btn-danger"
                  submitButtonVariant="danger"
                  messages={t.actions.cancelWithoutRefunding.modalActions}
                  action={cancelWithoutRefunding.bind(
                    null,
                    locale,
                    eventSlug,
                    order.id,
                  )}
                >
                  {t.actions.cancelWithoutRefunding.message}
                </ModalButton>
              </>
            )}
          </ButtonGroup>
        </CardBody>
      </Card>

      <Card className="mb-4">
        <CardBody>
          <CardTitle>{t.contactForm.title}</CardTitle>
          <form action={updateOrder.bind(null, locale, eventSlug, order.id)}>
            <ContactForm messages={translations} values={order} isAdmin />
            <SubmitButton>{t.actions.saveContactInformation}</SubmitButton>
          </form>
        </CardBody>
      </Card>

      <Card className="mb-4">
        <CardBody>
          <CardTitle>{sTamp.listTitle}</CardTitle>
          <DataTable columns={paymentStampColumns} rows={order.paymentStamps} />
        </CardBody>
      </Card>

      <Card className="mb-4">
        <CardBody>
          <CardTitle>{receipT.listTitle}</CardTitle>
          <DataTable columns={receiptColumns} rows={order.receipts} />
        </CardBody>
      </Card>
    </ViewContainer>
  );
}
