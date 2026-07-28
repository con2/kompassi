import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import {
  createMessageReplyTo,
  deleteMessageReplyTo,
  updateMessageReplyTo,
  updateProgramPreferences,
} from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment MessageReplyToRow on MessageReplyToType {
    id
    name
    email
  }
`);

const query = graphql(`
  query ProgramPreferences($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        publicFrom
        isSchedulePublic

        replyToAddresses {
          ...MessageReplyToRow
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

  const event = data.event;
  const program = data.event?.program;

  if (!event || !program) {
    notFound();
  }

  const tReplyTo = translations.Program.Message.ReplyTo;
  const replyToAddresses = program.replyToAddresses;

  const replyToFields: Field[] = [
    {
      slug: "name",
      type: "SingleLineText",
      title: tReplyTo.attributes.name.title,
      required: true,
    },
    {
      slug: "email",
      type: "SingleLineText",
      htmlType: "email",
      title: tReplyTo.attributes.email.title,
      required: true,
    },
  ];

  const replyToColumns: Column<(typeof replyToAddresses)[number]>[] = [
    { slug: "name", title: tReplyTo.attributes.name.title },
    { slug: "email", title: tReplyTo.attributes.email.title },
    {
      slug: "actions",
      title: translations.Common.actions,
      getCellContents: (replyTo) => (
        <>
          <ModalButton
            title={tReplyTo.actions.edit.title}
            messages={translations.Modal}
            action={updateMessageReplyTo.bind(
              null,
              locale,
              eventSlug,
              replyTo.id,
            )}
            className="btn btn-link p-0 link-subtle me-3"
          >
            <SchemaForm
              fields={replyToFields}
              values={replyTo}
              messages={translations.SchemaForm}
              locale={locale}
            />
          </ModalButton>
          <ModalButton
            title={tReplyTo.actions.delete.title}
            messages={translations.Modal}
            action={deleteMessageReplyTo.bind(
              null,
              locale,
              eventSlug,
              replyTo.id,
            )}
            className="btn btn-link p-0 link-subtle text-danger"
          >
            {tReplyTo.actions.delete.confirmation(replyTo.name)}
          </ModalButton>
        </>
      ),
    },
  ];

  const fields: Field[] = [
    {
      slug: "publicFrom",
      type: "DateTimeField",
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
              ? translations.SchemaForm.boolean.true
              : translations.SchemaForm.boolean.false}
          </p>
          <form action={updateProgramPreferences.bind(null, locale, eventSlug)}>
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

      <Card className="mb-3">
        <CardBody>
          <CardTitle>{tReplyTo.listTitle}</CardTitle>
          <p>{tReplyTo.description}</p>
          <DataTable columns={replyToColumns} rows={replyToAddresses} />
          <ModalButton
            title={tReplyTo.actions.create.title}
            messages={translations.Modal}
            action={createMessageReplyTo.bind(null, locale, eventSlug)}
            className="btn btn-outline-primary"
          >
            <SchemaForm
              fields={replyToFields}
              messages={translations.SchemaForm}
              locale={locale}
            />
          </ModalButton>
        </CardBody>
      </Card>
    </ProgramAdminView>
  );
}
