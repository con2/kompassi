"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { MessageDispatch } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const updateMessageMutation = graphql(`
  mutation UpdateMessage($input: UpdateMessageInput!) {
    updateMessage(input: $input) {
      message {
        id
      }
    }
  }
`);

export async function updateMessage(
  locale: string,
  eventSlug: string,
  messageId: string,
  formData: FormData,
) {
  const recipientFiltersRaw = formData.get("recipientFilters");
  const recipientFilters =
    typeof recipientFiltersRaw === "string" && recipientFiltersRaw
      ? JSON.parse(recipientFiltersRaw)
      : [];

  const replyToIdRaw = formData.get("replyToId");
  const replyToId =
    typeof replyToIdRaw === "string" && replyToIdRaw ? replyToIdRaw : null;

  await getClient().mutate({
    mutation: updateMessageMutation,
    variables: {
      input: {
        eventSlug,
        messageId,
        subject: String(formData.get("subject") ?? ""),
        body: String(formData.get("body") ?? ""),
        dispatch:
          (formData.get("dispatch") as MessageDispatch | null) ??
          MessageDispatch.PerPerson,
        replyToId,
        recipientFilters,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-messages/${messageId}`);
  revalidatePath(`/${locale}/${eventSlug}/program-messages`);
}

const sendMessageMutation = graphql(`
  mutation SendMessage($input: SendMessageInput!) {
    sendMessage(input: $input) {
      message {
        id
      }
    }
  }
`);

export async function sendMessage(
  locale: string,
  eventSlug: string,
  messageId: string,
  _formData: FormData,
) {
  await getClient().mutate({
    mutation: sendMessageMutation,
    variables: { input: { eventSlug, messageId } },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-messages/${messageId}`);
  revalidatePath(`/${locale}/${eventSlug}/program-messages`);
}

const expireMessageMutation = graphql(`
  mutation ExpireMessage($input: ExpireMessageInput!) {
    expireMessage(input: $input) {
      message {
        id
      }
    }
  }
`);

export async function expireMessage(
  locale: string,
  eventSlug: string,
  messageId: string,
  _formData: FormData,
) {
  await getClient().mutate({
    mutation: expireMessageMutation,
    variables: { input: { eventSlug, messageId } },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-messages/${messageId}`);
  revalidatePath(`/${locale}/${eventSlug}/program-messages`);
}

const deleteMessageMutation = graphql(`
  mutation DeleteMessage($input: DeleteMessageInput!) {
    deleteMessage(input: $input) {
      messageId
    }
  }
`);

export async function deleteMessage(
  locale: string,
  eventSlug: string,
  messageId: string,
  _formData: FormData,
) {
  await getClient().mutate({
    mutation: deleteMessageMutation,
    variables: { input: { eventSlug, messageId } },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-messages`);
  redirect(`/${eventSlug}/program-messages`);
}
