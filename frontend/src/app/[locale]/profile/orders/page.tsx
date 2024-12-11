import Link from "next/link";

import { payOrder } from "../../[eventSlug]/orders/[orderId]/actions";
import { confirmEmail } from "./actions";
import { graphql } from "@/__generated__";
import { PaymentStatus, ProfileOrderFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import formatMoney from "@/helpers/formatMoney";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileOrder on ProfileOrderType {
    id
    formattedOrderNumber
    createdAt
    totalPrice
    status
    electronicTicketsLink

    event {
      slug
      name
    }
  }
`);

const query = graphql(`
  query ProfileOrders {
    profile {
      tickets {
        orders {
          ...ProfileOrder
        }

        haveUnlinkedOrders
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.profile;

  return {
    title: getPageTitle({ viewTitle: t.title, translations }),
  };
}

export const revalidate = 0;

export default async function OwnResponsesPage({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.profile;
  const staT = translations.Tickets.orderStatus;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query });

  const columns: Column<ProfileOrderFragment>[] = [
    {
      slug: "orderNumber",
      title: t.attributes.orderNumber,
      getCellContents: (order) => (
        <Link
          className="link-subtle"
          href={`/profile/orders/${order.event.slug}/${order.id}`}
        >
          {order.formattedOrderNumber}
        </Link>
      ),
    },
    {
      slug: "createdAt",
      title: t.attributes.createdAt,
      getCellContents: (order) => (
        <FormattedDateTime
          value={order.createdAt}
          locale={locale}
          scope={order.event}
          session={session}
        />
      ),
    },
    {
      slug: "eventName",
      title: t.attributes.eventName,
      getCellContents: (order) => order.event.name,
    },
    {
      slug: "totalPrice",
      title: t.attributes.totalPrice,
      getCellContents: (order) => formatMoney(order.totalPrice),
    },
    {
      slug: "status",
      title: t.attributes.status,
      getCellContents: (order) => staT[order.status].shortTitle,
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCellContents: (order) => (
        <>
          {order.status === PaymentStatus.Paid &&
            order.electronicTicketsLink && (
              <Link
                className="btn btn-sm btn-primary"
                href={order.electronicTicketsLink}
              >
                {t.actions.downloadTickets.title}
              </Link>
            )}
          {order.status === PaymentStatus.Pending && (
            <button
              className="btn btn-sm btn-primary"
              onClick={payOrder.bind(null, order.event.slug, order.id, locale)}
            >
              {t.actions.pay.title}
            </button>
          )}
        </>
      ),
    },
  ];

  const orders = data.profile?.tickets?.orders ?? [];
  const haveUnlinkedOrders = data.profile?.tickets?.haveUnlinkedOrders;

  return (
    <ViewContainer>
      <ViewHeading>{t.title}</ViewHeading>
      <p>{t.description}</p>
      <DataTable
        rows={orders}
        columns={columns}
        getTotalMessage={t.attributes.totalOrders}
      />
      {haveUnlinkedOrders && (
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">{t.haveUnlinkedOrders.title}</h5>
            <p className="card-text">{t.haveUnlinkedOrders.message}</p>
            <ModalButton
              className="btn btn-primary"
              label={t.actions.confirmEmail.title + "…"}
              title={t.actions.confirmEmail.title}
              messages={t.actions.confirmEmail.modalActions}
              action={confirmEmail.bind(null, locale)}
            >
              {t.actions.confirmEmail.description}
            </ModalButton>
          </div>
        </div>
      )}
    </ViewContainer>
  );
}
