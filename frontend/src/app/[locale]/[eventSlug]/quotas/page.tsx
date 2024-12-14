import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { QuotaListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/SignInRequired";
import TicketAdminTabs from "@/components/tickets/admin/TicketAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment QuotaList on FullQuotaType {
    id
    title: name
    countPaid
    countReserved
    countAvailable
    countTotal
  }
`);

const query = graphql(`
  query QuotaList($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        quotas {
          ...QuotaList
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
  const t = translations.Tickets.Product;

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

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

export default async function QuotasPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.Product;
  const quoT = translations.Tickets.Quota;

  // TODO encap
  const session = await auth();
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
  const quotas = data.event.tickets.quotas;

  // we cheat and use the translations from the products page so as to not have to repeat them :)
  const columns: Column<QuotaListFragment>[] = [
    {
      slug: "title",
      title: quoT.singleTitle,
      getCellContents: (quota) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/quotas/${quota.id}`}
        >
          {quota.title}
        </Link>
      ),
    },
    {
      slug: "countPaid",
      title: t.attributes.countPaid,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countReserved",
      title: t.attributes.countReserved.title,
      className: "text-end align-middle col-1",
      getHeaderContents: () => (
        <abbr title={t.attributes.countReserved.description}>
          {t.attributes.countReserved.title}
        </abbr>
      ),
    },
    {
      slug: "countAvailable",
      title: t.attributes.countAvailable,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countTotal",
      title: t.attributes.countTotal,
      className: "text-end align-middle col-2",
    },
  ];

  return (
    <ViewContainer>
      <ViewHeading>
        {translations.Tickets.admin.title}
        <ViewHeading.Sub>{quoT.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <TicketAdminTabs
        eventSlug={eventSlug}
        active="quotas"
        translations={translations}
      />

      <DataTable rows={quotas} columns={columns} />
    </ViewContainer>
  );
}
