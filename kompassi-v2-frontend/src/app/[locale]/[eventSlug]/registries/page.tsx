import {
  Column,
  DataTable,
  SignInRequired,
  ModalButton,
} from "@con2/components";
import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { RegistryListFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { createRegistry } from "./actions";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment RegistryList on FullRegistryType {
    slug
    title(lang: $locale)
    defaultRetentionPeriodDays
  }
`);

const query = graphql(`
  query RegistryList($eventSlug: String!, $locale: String!) {
    event(slug: $eventSlug) {
      name
      slug

      involvement {
        registries {
          ...RegistryList
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
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Registry;

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.involvement) {
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

export default async function RegistriesPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Registry;

  const session = await auth();
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.involvement) {
    notFound();
  }

  const event = data.event;
  const registries = data.event.involvement.registries;

  const columns: Column<RegistryListFragment>[] = [
    {
      slug: "title",
      title: t.singleTitle,
      getCellContents: (registry) => (
        <Link
          className="link-subtle"
          href={`/${event.slug}/registries/${registry.slug}`}
        >
          {registry.title}
        </Link>
      ),
    },
    {
      slug: "slug",
      title: t.attributes.slug,
      getCellContents: (registry) => <em>{registry.slug}</em>,
    },
    {
      slug: "defaultRetentionPeriodDays",
      title: t.attributes.defaultRetentionPeriodDays.title,
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCellContents: (registry) => (
        <Link
          href={`/${eventSlug}/people?registry=${registry.slug}`}
          className="btn btn-sm btn-outline-primary"
        >
          {t.attributes.peopleInThisEvent}…
        </Link>
      ),
    },
  ];

  const createRegistryFields: Field[] = [
    {
      slug: "slug",
      title: t.attributes.slug,
      type: "SingleLineText",
      required: true,
    },
    {
      slug: "title_en",
      title: t.attributes.title.en,
      type: "SingleLineText",
      required: true,
    },
    {
      slug: "title_fi",
      title: t.attributes.title.fi,
      type: "SingleLineText",
      required: true,
    },
    {
      slug: "title_sv",
      title: t.attributes.title.sv,
      type: "SingleLineText",
      required: true,
    },
  ];

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="registries"
      searchParams={searchParams}
      actions={
        <ModalButton
          title={t.actions.newRegistry.title}
          messages={t.actions.newRegistry.modalActions}
          action={createRegistry.bind(null, locale, eventSlug)}
          className="btn btn-outline-primary"
        >
          <SchemaForm
            fields={createRegistryFields}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      }
    >
      <DataTable rows={registries} columns={columns} />
    </InvolvementAdminView>
  );
}
