import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { QuotaListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { createQuota } from "./actions";

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
  params: Promise<{
    locale: string;
    eventSlug: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
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

export default async function QuotasPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const producT = translations.Tickets.Product;
  const t = translations.Tickets.Quota;

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

  const columns: Column<QuotaListFragment>[] = [
    {
      slug: "title",
      title: t.singleTitle,
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
      title: producT.clientAttributes.countPaid,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countReserved",
      title: producT.clientAttributes.countReserved.title,
      className: "text-end align-middle col-1",
      getHeaderContents: () => (
        <abbr title={producT.clientAttributes.countReserved.description}>
          {producT.clientAttributes.countReserved.title}
        </abbr>
      ),
    },
    {
      slug: "countAvailable",
      title: producT.clientAttributes.countAvailable,
      className: "text-end align-middle col-1",
    },
    {
      slug: "countTotal",
      title: producT.clientAttributes.countTotal,
      className: "text-end align-middle col-2",
    },
  ];

  const newQuotaFields: Field[] = [
    {
      slug: "name",
      title: t.attributes.name,
      type: "SingleLineText",
    },
    {
      slug: "quota",
      title: t.attributes.countTotal.title,
      helpText: t.attributes.countTotal.helpTextNew,
      type: "NumberField",
    },
  ];

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      active="quotas"
      actions={
        <ModalButton
          title={t.actions.newQuota.title}
          messages={t.actions.newQuota.modalActions}
          action={createQuota.bind(null, locale, eventSlug)}
          className="btn btn-outline-primary"
        >
          <SchemaForm
            fields={newQuotaFields}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      }
    >
      <DataTable rows={quotas} columns={columns} />
    </TicketsAdminView>
  );
}
