import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramMessageListRow on MessageType {
    id
    subject
    state
    dispatch
    createdAt
    sentAt
    recipientCount
  }
`);

const query = graphql(`
  query ProgramMessagesPage($eventSlug: String!) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        messages {
          ...ProgramMessageListRow
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

  const { data } = await getClient().query({ query, variables: { eventSlug } });

  return {
    title: getPageTitle({
      translations,
      event: data.event,
      viewTitle: translations.Program.Message.listTitle,
    }),
  };
}

export default async function ProgramMessagesPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query, variables: { eventSlug } });

  const event = data.event;
  if (!event || !event.program) {
    notFound();
  }

  const messages = event.program.messages;

  const columns: Column<(typeof messages)[number]>[] = [
    {
      slug: "subject",
      title: t.attributes.subject.title,
      getCellContents: (message) => (
        <a href={`/${eventSlug}/program-messages/${message.id}`}>
          {message.subject || t.attributes.subject.noSubject}
        </a>
      ),
      className: "col-4 align-middle",
    },
    {
      slug: "state",
      title: t.attributes.state.title,
      getCellContents: (message) => t.attributes.state.choices[message.state],
      className: "col-2 align-middle",
    },
    {
      slug: "createdAt",
      title: t.attributes.createdAt.title,
      getCellContents: (message) => (
        <FormattedDateTime
          value={message.createdAt}
          locale={locale}
          scope={event}
          session={session}
        />
      ),
      className: "col-2 align-middle",
    },
    {
      slug: "recipientCount",
      title: t.attributes.recipientCount.title,
      getCellContents: (message) =>
        t.attributes.recipientCount.value(message.recipientCount),
      className: "col-2 align-middle",
    },
  ];

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active="programMessages"
      searchParams={searchParams}
      actions={
        <Link
          href={`/${eventSlug}/program-messages/new`}
          className="btn btn-outline-primary"
        >
          {t.actions.newMessage.title}…
        </Link>
      }
    >
      <DataTable
        columns={columns}
        rows={messages}
        getTotalMessage={t.attributes.count}
      />
    </ProgramAdminView>
  );
}
