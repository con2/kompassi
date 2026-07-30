"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { MessageDispatch } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import parseRecipientFilters from "../parseRecipientFilters";

const createMessageMutation = graphql(`
  mutation CreateMessage($input: CreateMessageInput!) {
    createMessage(input: $input) {
      message {
        id
      }
    }
  }
`);

export async function createMessage(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const recipientFilters = parseRecipientFilters(
    formData.get("recipientFilters"),
  );

  const replyToIdRaw = formData.get("replyToId");
  const replyToId =
    typeof replyToIdRaw === "string" && replyToIdRaw ? replyToIdRaw : null;

  const result = await getClient().mutate({
    mutation: createMessageMutation,
    variables: {
      input: {
        eventSlug,
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

  revalidatePath(`/${locale}/${eventSlug}/program-messages`);

  const newMessageId = result.data?.createMessage?.message?.id;
  redirect(`/${eventSlug}/program-messages/${newMessageId ?? ""}`);
}
