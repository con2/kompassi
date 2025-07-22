import Link from "next/link";

import { notFound } from "next/navigation";
import { Fragment } from "react";
import Accordion from "react-bootstrap/Accordion";
import AccordionBody from "react-bootstrap/AccordionBody";
import AccordionHeader from "react-bootstrap/AccordionHeader";
import AccordionItem from "react-bootstrap/AccordionItem";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import {
  cancelAndRefundOrder,
  markOrderAsPaid,
  resendConfirmation,
  updateOrder,
} from "./actions";
import { graphql } from "@/__generated__";
import {
  AdminOrderCodeFragment,
  AdminOrderPaymentStampFragment,
  AdminOrderReceiptFragment,
  CodeStatus,
  PaymentStatus,
  RefundType,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import Messages from "@/components/errors/Messages";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import ContactForm from "@/components/tickets/ContactForm";
import ProductsTable from "@/components/tickets/ProductsTable";
import TicketsAdminTabs from "@/components/tickets/TicketsAdminTabs";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment AdminOrderPaymentStamp on LimitedPaymentStampType {
    id
    createdAt
    correlationId
    provider
    type
    status
    data
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

graphql(`
  fragment AdminOrderCode on LimitedCodeType {
    code
    literateCode
    status
    usedOn
    productText
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
          canRefund
          canRefundManually
          canMarkAsPaid
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
          codes {
            ...AdminOrderCode
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    orderId: string;
  }>;
  searchParams: Promise<{
    success?: string;
    error?: string;
  }>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
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

export default async function AdminOrderPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, orderId } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const sTamp = translations.Tickets.PaymentStamp;
  const receipT = translations.Tickets.Receipt;
  const producT = translations.Tickets.Product;
  const codeT = translations.Tickets.Code;
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
      getCellContents: (stamp) => {
        const { __typename, ...interestingFields } = stamp;
        return (
          <ModalButton
            title={sTamp.attributes.type.choices[stamp.type]}
            label={
              <FormattedDateTime
                value={stamp.createdAt}
                locale={locale}
                scope={event}
                session={session}
              />
            }
            className="btn btn-link link-subtle m-0 p-0"
            submitButtonVariant="danger"
            messages={sTamp.actions.view.modalActions}
          >
            {sTamp.actions.view.message}
            <pre>{JSON.stringify(interestingFields, null, 2)}</pre>
          </ModalButton>
        );
      },
      className: "col-2 align-middle",
    },
    {
      slug: "correlationId",
      title: sTamp.attributes.correlationId,
      className: "col-3 align-middle",
      getCellContents: (stamp) => <small>{stamp.correlationId}</small>,
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
      className: "col-3 align-middle",
      getCellContents: (receipt) => <small>{receipt.correlationId}</small>,
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

  const codeColumns: Column<AdminOrderCodeFragment>[] = [
    {
      slug: "productText",
      title: codeT.attributes.productText,
      className: "col-3 align-middle",
      scope: "row",
    },
    {
      slug: "code",
      title: codeT.attributes.code,
      className: "col align-middle",
    },
    {
      slug: "literateCode",
      title: codeT.attributes.literateCode,
      className: "col-3 align-middle",
      // getCellContents: (code) => <small>{code.literateCode}</small>,
    },
    {
      slug: "status",
      title: codeT.attributes.status.title,
      className: "col align-middle",
      getCellContents(code) {
        if (code.status == CodeStatus.Used) {
          return (
            <>
              {codeT.attributes.status.choices[code.status]}{" "}
              <FormattedDateTime
                value={code.usedOn}
                locale={locale}
                scope={event}
                session={session}
              />
            </>
          );
        } else {
          return <>{codeT.attributes.status.choices[code.status]}</>;
        }
      },
    },
  ];

  const event = data.event;
  const order = data.event.tickets.order;
  const { shortTitle: paymentStatus } =
    t.attributes.status.choices[order.status];

  const queryString = new URLSearchParams(searchParams).toString();

  const actions = [
    {
      slug: "viewOrderPage",
      isShown: true,
      getElement: () => (
        <Link
          className="btn btn-primary"
          target="_blank"
          rel="noopener noreferrer"
          href={`/${event.slug}/orders/${order.id}`}
        >
          {t.actions.viewOrderPage}…
        </Link>
      ),
    },
    {
      slug: "viewTickets",
      isShown: !!order.eticketsLink,
      getElement: () => (
        <a
          href={order.eticketsLink ?? ""}
          target="_blank"
          rel="noopener noreferer"
          className="btn btn-primary"
        >
          {t.actions.viewTickets}…
        </a>
      ),
    },
    {
      slug: "resendOrderConfirmation",
      isShown: order.status === PaymentStatus.Paid,
      getElement: () => (
        <ModalButton
          title={t.actions.resendOrderConfirmation.title}
          className="btn btn-success"
          submitButtonVariant="success"
          messages={t.actions.resendOrderConfirmation.modalActions}
          action={resendConfirmation.bind(null, locale, eventSlug, order.id)}
        >
          {t.actions.resendOrderConfirmation.message(order.email)}
        </ModalButton>
      ),
    },
    {
      slug: "markAsPaid",
      isShown: order.canMarkAsPaid,
      getElement: () => (
        <ModalButton
          title={t.actions.markAsPaid.title}
          className="btn btn-success"
          submitButtonVariant="success"
          messages={t.actions.markAsPaid.modalActions}
          action={markOrderAsPaid.bind(null, locale, eventSlug, order.id)}
        >
          {t.actions.markAsPaid.message}
        </ModalButton>
      ),
    },
    {
      slug: "cancelWithoutRefunding",
      isShown:
        order.status === PaymentStatus.NotStarted ||
        order.status === PaymentStatus.Pending ||
        order.status === PaymentStatus.Failed ||
        order.status === PaymentStatus.Paid,
      getElement: () => (
        <ModalButton
          label={t.actions.cancelWithoutRefunding.label + "…"}
          title={t.actions.cancelWithoutRefunding.title}
          className="btn btn-danger"
          submitButtonVariant="danger"
          messages={t.actions.cancelWithoutRefunding.modalActions}
          action={cancelAndRefundOrder.bind(
            null,
            locale,
            eventSlug,
            order.id,
            RefundType.None,
          )}
        >
          {t.actions.cancelWithoutRefunding.message}
        </ModalButton>
      ),
    },
    {
      slug: "cancelAndRefund",
      isShown: order.canRefund && order.status === PaymentStatus.Paid,
      getElement: () => (
        <ModalButton
          title={t.actions.cancelAndRefund.title}
          label={t.actions.cancelAndRefund.label + "…"}
          className="btn btn-danger"
          submitButtonVariant="danger"
          messages={t.actions.cancelAndRefund.modalActions}
          action={cancelAndRefundOrder.bind(
            null,
            locale,
            eventSlug,
            order.id,
            RefundType.Provider,
          )}
        >
          {t.actions.cancelAndRefund.message}
        </ModalButton>
      ),
    },
    {
      slug: "refundCancelledOrder",
      isShown: order.canRefund && order.status === PaymentStatus.Cancelled,
      getElement: () => (
        <ModalButton
          title={t.actions.refundCancelledOrder.title}
          className="btn btn-danger"
          submitButtonVariant="danger"
          messages={t.actions.refundCancelledOrder.modalActions}
          action={cancelAndRefundOrder.bind(
            null,
            locale,
            eventSlug,
            order.id,
            RefundType.Provider,
          )}
        >
          {t.actions.refundCancelledOrder.message}
        </ModalButton>
      ),
    },
    {
      slug: "retryRefund",
      isShown: order.canRefund && order.status === PaymentStatus.RefundFailed,
      getElement: () => (
        <ModalButton
          title={t.actions.retryRefund.title}
          className="btn btn-danger"
          submitButtonVariant="danger"
          messages={t.actions.retryRefund.modalActions}
          action={cancelAndRefundOrder.bind(
            null,
            locale,
            eventSlug,
            order.id,
            RefundType.Provider,
          )}
        >
          {t.actions.retryRefund.message}
        </ModalButton>
      ),
    },
    {
      slug: "refundManually",
      isShown: order.canRefundManually,
      getElement: () => (
        <ModalButton
          title={t.actions.refundManually.title}
          className="btn btn-danger"
          submitButtonVariant="danger"
          messages={t.actions.refundManually.modalActions}
          action={cancelAndRefundOrder.bind(
            null,
            locale,
            eventSlug,
            order.id,
            RefundType.Manual,
          )}
        >
          {t.actions.refundManually.message}
        </ModalButton>
      ),
    },
  ];

  const visibleActions = actions.filter((action) => action.isShown);

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      searchParams={searchParams}
      active="orders"
    >
      <div className="d-flex">
        <h3 className="mt-3 mb-3">
          {t.singleTitle(order.formattedOrderNumber, paymentStatus)}
        </h3>

        {!!visibleActions.length && (
          <div className="mt-3 mb-3 ms-auto">
            <ButtonGroup>
              {visibleActions.map((action) => (
                <Fragment key={action.slug}>{action.getElement()}</Fragment>
              ))}
            </ButtonGroup>
          </div>
        )}
      </div>

      <Accordion defaultActiveKey="products">
        <AccordionItem eventKey="products">
          <AccordionHeader>{producT.listTitle}</AccordionHeader>
          <AccordionBody>
            <ProductsTable
              order={order}
              messages={translations.Tickets}
              compact
              className="m-0"
            />
          </AccordionBody>
        </AccordionItem>
        <AccordionItem eventKey="contact">
          <AccordionHeader>{t.contactForm.title}</AccordionHeader>
          <AccordionBody>
            <form action={updateOrder.bind(null, locale, eventSlug, order.id)}>
              <ContactForm messages={translations} values={order} isAdmin />
              <SubmitButton>{t.actions.saveContactInformation}</SubmitButton>
            </form>
          </AccordionBody>
        </AccordionItem>

        <AccordionItem eventKey="codes">
          <AccordionHeader>{codeT.listTitle}</AccordionHeader>
          <AccordionBody>
            <DataTable columns={codeColumns} rows={order.codes} />
          </AccordionBody>
        </AccordionItem>

        <AccordionItem eventKey="paymentStamps">
          <AccordionHeader>{sTamp.listTitle}</AccordionHeader>
          <AccordionBody>
            <DataTable
              columns={paymentStampColumns}
              rows={order.paymentStamps}
            />
          </AccordionBody>
        </AccordionItem>

        <AccordionItem eventKey="receipts">
          <AccordionHeader>{receipT.listTitle}</AccordionHeader>
          <AccordionBody>
            <DataTable columns={receiptColumns} rows={order.receipts} />
          </AccordionBody>
        </AccordionItem>
      </Accordion>
    </TicketsAdminView>
  );
}
