import { notFound } from "next/navigation";

import {
  deleteMessage,
  expireMessage,
  sendMessage,
  updateMessage,
} from "./actions";
import MessageComposeCard from "../MessageComposeCard";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { ButtonGroup } from "react-bootstrap";

graphql(`
  fragment MessageCompose on MessageType {
    id
    subject
    body
    dispatch
    state
    createdAt
    sentAt
    expiredAt
    recipientFilters
    recipientCount
    replyTo {
      id
    }
  }
`);

const query = graphql(`
  query ProgramMessageComposePage(
    $eventSlug: String!
    $messageId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        message(id: $messageId) {
          ...MessageCompose
        }
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
    messageId: string;
  }>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, messageId } = params;
  const translations = getTranslations(locale);

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, messageId, locale },
  });

  return {
    title: getPageTitle({
      translations,
      event: data.event,
      viewTitle: translations.Program.Message.listTitle,
      subject: data.event?.program?.message?.subject,
    }),
  };
}

export default async function ProgramMessageComposePage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, messageId } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, messageId, locale },
  });

  const event = data.event;
  const message = event?.program?.message;
  const replyToAddresses = event?.program?.replyToAddresses ?? [];
  const recipientDimensions = event?.program?.recipientDimensions ?? [];

  if (!event || !event.program || !message) {
    notFound();
  }

  const isSent = message.state !== "DRAFT";
  const formId = "message-compose-form";

  const values = {
    subject: message.subject,
    dispatch: message.dispatch,
    replyToId: message.replyTo?.id ?? "",
    body: message.body,
  };

  const recipientGroups = (message.recipientFilters ?? []) as {
    dimension: string;
    values?: string[] | null;
  }[][];

  return (
    <ProgramAdminView
      event={event}
      translations={translations}
      active="programMessages"
      searchParams={{}}
      actions={
        <ButtonGroup>
          <ModalButton
            title={t.actions.send.title}
            messages={t.actions.send.modalActions}
            action={sendMessage.bind(null, locale, eventSlug, messageId)}
            className="btn btn-outline-primary"
          >
            {isSent
              ? t.actions.send.confirmationResend
              : t.actions.send.confirmation}
          </ModalButton>
          {isSent && message.state === "ACTIVE" && (
            <ModalButton
              title={t.actions.expire.title}
              messages={t.actions.expire.modalActions}
              action={expireMessage.bind(null, locale, eventSlug, messageId)}
              className="btn btn-outline-warning"
            >
              {t.actions.expire.confirmation}
            </ModalButton>
          )}
          {!isSent && (
            <ModalButton
              title={t.actions.delete.title}
              messages={t.actions.delete.modalActions}
              action={deleteMessage.bind(null, locale, eventSlug, messageId)}
              className="btn btn-outline-danger"
            >
              {t.actions.delete.confirmation}
            </ModalButton>
          )}
        </ButtonGroup>
      }
    >
      <MessageComposeCard
        formId={formId}
        action={updateMessage.bind(null, locale, eventSlug, messageId)}
        translations={translations}
        locale={locale}
        replyToAddresses={replyToAddresses}
        recipientDimensions={recipientDimensions}
        recipientGroups={recipientGroups}
        recipientCount={message.recipientCount}
        values={values}
        saveLabel={isSent ? t.actions.saveChanges : t.actions.saveDraft}
        saveHelpText={
          isSent ? t.actions.alreadySentWarning : t.actions.saveDraftHelpText
        }
      />
    </ProgramAdminView>
  );
}
