import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { updateTicketsPreferences } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import TicketsAdminView from "@/components/tickets/TicketsAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query TicketsPreferences($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      tickets {
        contactEmail
        termsAndConditionsUrlEn
        termsAndConditionsUrlFi
        termsAndConditionsUrlSv
        cancellationPeriodDays
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

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  return {
    title: getPageTitle({
      translations,
      event: data.event,
      viewTitle: translations.Tickets.admin.preferences.title,
    }),
  };
}

export default async function TicketsPreferencesPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Tickets.admin.preferences;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  const event = data.event;
  const tickets = data.event?.tickets;

  if (!event || !tickets) {
    notFound();
  }

  const fields: Field[] = [
    {
      slug: "contactEmail",
      type: "SingleLineText",
      title: t.attributes.contactEmail.title,
      helpText: t.attributes.contactEmail.helpText,
      required: false,
    },
    {
      slug: "termsAndConditionsUrlEn",
      type: "SingleLineText",
      title: t.attributes.termsAndConditionsUrl.en,
      required: false,
    },
    {
      slug: "termsAndConditionsUrlFi",
      type: "SingleLineText",
      title: t.attributes.termsAndConditionsUrl.fi,
      required: false,
    },
    {
      slug: "termsAndConditionsUrlSv",
      type: "SingleLineText",
      title: t.attributes.termsAndConditionsUrl.sv,
      required: false,
    },
    {
      slug: "cancellationPeriodDays",
      type: "NumberField",
      title: t.attributes.cancellationPeriodDays.title,
      helpText: t.attributes.cancellationPeriodDays.helpText,
      required: false,
    },
  ];

  const values = {
    contactEmail: tickets.contactEmail ?? "",
    termsAndConditionsUrlEn: tickets.termsAndConditionsUrlEn ?? "",
    termsAndConditionsUrlFi: tickets.termsAndConditionsUrlFi ?? "",
    termsAndConditionsUrlSv: tickets.termsAndConditionsUrlSv ?? "",
    cancellationPeriodDays: tickets.cancellationPeriodDays,
  };

  return (
    <TicketsAdminView
      translations={translations}
      event={event}
      active="preferences"
      searchParams={searchParams}
    >
      <Card className="mt-3 mb-3">
        <CardBody>
          <form action={updateTicketsPreferences.bind(null, locale, eventSlug)}>
            <SchemaForm
              fields={fields}
              values={values}
              messages={translations.SchemaForm}
              locale={locale}
            />
            <SubmitButton>
              {translations.Common.standardActions.save}
            </SubmitButton>
          </form>
        </CardBody>
      </Card>
    </TicketsAdminView>
  );
}
