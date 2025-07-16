import Link from "next/link";

import {
  cancelOrder,
  payOrder,
} from "../../[eventSlug]/orders/[orderId]/actions";
import { confirmEmail } from "./actions";
import { graphql } from "@/__generated__";
import { ProfileOrderFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import Messages from "@/components/errors/Messages";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ModalButton from "@/components/ModalButton";
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
    eticketsLink
    canPay
    canCancel

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
  searchParams: {
    success?: string;
    error?: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets;

  return {
    title: getPageTitle({ viewTitle: t.profile.title, translations }),
  };
}

export const revalidate = 0;

export default async function ProfileOrdersPage({
  params,
  searchParams,
}: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Order;
  const profileT = translations.Tickets.profile;
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query });

  const columns: Column<ProfileOrderFragment>[] = [
    {
      slug: "orderNumber",
      title: t.attributes.orderNumberAbbr,
      className: "col-1 align-middle",
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
      title: t.attributes.status.title,
      getCellContents: (order) =>
        t.attributes.status.choices[order.status].shortTitle,
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCellContents: (order) => (
        <>
          {order.eticketsLink && (
            <Link
              className="btn btn-link link-subtle p-0 ms-2"
              href={order.eticketsLink}
            >
              🎫 {t.actions.viewTickets}
            </Link>
          )}
          {order.canPay && (
            <form
              action={payOrder.bind(null, locale, order.event.slug, order.id)}
            >
              <button
                className="btn btn-link link-subtle p-0 ms-2"
                type="submit"
              >
                💳 {t.actions.pay}
              </button>
            </form>
          )}
          {order.canCancel && (
            <ModalButton
              className="btn btn-link link-subtle p-0 ms-2"
              label={<>❌ {t.actions.ownerCancel.label}…</>}
              title={t.actions.ownerCancel.title}
              messages={t.actions.ownerCancel.modalActions}
              action={cancelOrder.bind(
                null,
                locale,
                order.event.slug,
                order.id,
              )}
            >
              {t.actions.ownerCancel.message}
            </ModalButton>
          )}
        </>
      ),
    },
  ];

  const orders = data.profile?.tickets?.orders ?? [];
  const haveUnlinkedOrders = data.profile?.tickets?.haveUnlinkedOrders;

  return (
    <ViewContainer>
      <ViewHeading>{profileT.title}</ViewHeading>
      <Messages searchParams={searchParams} messages={t.profileMessages} />
      <p>{profileT.message}</p>
      {haveUnlinkedOrders && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">{profileT.haveUnlinkedOrders.title}</h5>
            <p className="card-text">{profileT.haveUnlinkedOrders.message}</p>
            <ModalButton
              className="btn btn-primary"
              label={profileT.actions.confirmEmail.title + "…"}
              title={profileT.actions.confirmEmail.title}
              messages={profileT.actions.confirmEmail.modalActions}
              action={confirmEmail.bind(null, locale)}
            >
              {profileT.actions.confirmEmail.description}
            </ModalButton>
          </div>
        </div>
      )}
      {orders.length > 0 && (
        <DataTable rows={orders} columns={columns} responsive="md">
          <tfoot>
            <tr>
              <td colSpan={columns.length}>
                {t.attributes.totalOrders(orders.length)}
              </td>
            </tr>
          </tfoot>
        </DataTable>
      )}
      {orders.length === 0 && !haveUnlinkedOrders && <p>{profileT.noOrders}</p>}
    </ViewContainer>
  );
}
