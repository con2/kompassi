import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { updateProgramPreferences } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramPreferences($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        publicFrom
        isSchedulePublic
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
      viewTitle: translations.Program.preferencesAdmin.title,
    }),
  };
}

export default async function ProgramPreferencesPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.preferencesAdmin;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug },
  });

  if (!data.event?.program) {
    notFound();
  }

  const { event } = data;
  const { program } = event;

  const fields: Field[] = [
    {
      slug: "publicFrom",
      type: "DateTime",
      title: t.attributes.publicFrom.title,
      helpText: t.attributes.publicFrom.helpText,
      required: false,
    },
  ];

  const values = {
    publicFrom: program.publicFrom ?? "",
  };

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active="preferences"
      searchParams={searchParams}
    >
      <Card className="mt-3 mb-3">
        <CardBody>
          <p>
            <strong>{t.attributes.isSchedulePublic.title}:</strong>{" "}
            {program.isSchedulePublic
              ? translations.Common.boolean.true
              : translations.Common.boolean.false}
          </p>
          <form action={updateProgramPreferences.bind(null, locale, eventSlug)}>
            <SchemaForm
              fields={fields}
              values={values}
              messages={translations.SchemaForm}
            />
            <SubmitButton>
              {translations.Common.standardActions.save}
            </SubmitButton>
          </form>
        </CardBody>
      </Card>
    </ProgramAdminView>
  );
}
