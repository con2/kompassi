import { SignInRequired } from "@con2/components";
import { notFound } from "next/navigation";

import { createMessage } from "./actions";
import MessageComposeCard from "../MessageComposeCard";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramMessageNewPage($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        replyToAddresses {
          id
          name
          email
        }
        recipientDimensions {
          ...DimensionValueSelect
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
    variables: { eventSlug, locale },
  });

  return {
    title: getPageTitle({
      translations,
      event: data.event,
      viewTitle: translations.Program.Message.actions.newMessage.title,
    }),
  };
}

/// Renders the compose form for a message that does not exist in the database yet.
/// It is only created (via CreateMessage) when this form is first saved - viewing this
/// page, or navigating away from it, never commits anything.
export default async function ProgramMessageNewPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message;

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

  const event = data.event;
  if (!event || !event.program) {
    notFound();
  }

  const replyToAddresses = event.program.replyToAddresses;
  const recipientDimensions = event.program.recipientDimensions;

  const values = {
    subject: "",
    dispatch: "PER_PERSON",
    replyToId: "",
    body: "",
  };

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active="programMessages"
      searchParams={{}}
    >
      <MessageComposeCard
        formId="message-compose-form"
        action={createMessage.bind(null, locale, eventSlug)}
        translations={translations}
        locale={locale}
        replyToAddresses={replyToAddresses}
        recipientDimensions={recipientDimensions}
        recipientGroups={[]}
        recipientCount={null}
        values={values}
        saveLabel={t.actions.saveDraft}
        saveHelpText={t.actions.saveDraftHelpText}
      />
    </ProgramAdminView>
  );
}
