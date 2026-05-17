import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { updateInvolvementPreferences } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query InvolvementPreferences($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      involvement {
        shirtsFrozenAt
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
      viewTitle: translations.Involvement.preferencesAdmin.title,
    }),
  };
}

export default async function InvolvementPreferencesPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Involvement.preferencesAdmin;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  const event = data.event;
  const involvement = data.event?.involvement;

  if (!event || !involvement) {
    notFound();
  }

  const fields: Field[] = [
    {
      slug: "shirtsFrozenAt",
      type: "DateTimeField",
      title: t.attributes.shirtsFrozenAt.title,
      helpText: t.attributes.shirtsFrozenAt.helpText,
      required: false,
    },
  ];

  const values = {
    shirtsFrozenAt: involvement.shirtsFrozenAt ?? "",
  };

  return (
    <InvolvementAdminView
      event={event}
      translations={translations}
      active="preferences"
      searchParams={searchParams}
    >
      <Card className="mt-3 mb-3">
        <CardBody>
          <form
            action={updateInvolvementPreferences.bind(null, locale, eventSlug)}
          >
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
    </InvolvementAdminView>
  );
}
