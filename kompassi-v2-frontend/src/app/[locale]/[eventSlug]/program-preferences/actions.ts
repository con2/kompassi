"use server";

import { decodeBoolean } from "@con2/components/helpers";
import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramPreferences($input: UpdateProgramPreferencesInput!) {
    updateProgramPreferences(input: $input) {
      preferences {
        publicFrom
        isSchedulePublic
        protectResponses
      }
    }
  }
`);

export async function updateProgramPreferences(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const publicFromRaw = formData.get("publicFrom");
  const publicFrom =
    publicFromRaw && typeof publicFromRaw === "string" && publicFromRaw !== ""
      ? publicFromRaw
      : null;
  const protectResponses = decodeBoolean(
    (formData.get("protectResponses") as string | null) || "false",
  );

  await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        publicFrom,
        protectResponses,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-preferences`);
  revalidatePath(`/${locale}/${eventSlug}/program`);
}

const createMessageReplyToMutation = graphql(`
  mutation CreateMessageReplyTo($input: CreateMessageReplyToInput!) {
    createMessageReplyTo(input: $input) {
      replyTo {
        id
      }
    }
  }
`);

export async function createMessageReplyTo(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: createMessageReplyToMutation,
    variables: {
      input: {
        eventSlug,
        name: String(formData.get("name") ?? ""),
        email: String(formData.get("email") ?? ""),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-preferences`);
}

const updateMessageReplyToMutation = graphql(`
  mutation UpdateMessageReplyTo($input: UpdateMessageReplyToInput!) {
    updateMessageReplyTo(input: $input) {
      replyTo {
        id
      }
    }
  }
`);

export async function updateMessageReplyTo(
  locale: string,
  eventSlug: string,
  replyToId: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation: updateMessageReplyToMutation,
    variables: {
      input: {
        eventSlug,
        replyToId,
        name: String(formData.get("name") ?? ""),
        email: String(formData.get("email") ?? ""),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-preferences`);
}

const deleteMessageReplyToMutation = graphql(`
  mutation DeleteMessageReplyTo($input: DeleteMessageReplyToInput!) {
    deleteMessageReplyTo(input: $input) {
      replyToId
    }
  }
`);

export async function deleteMessageReplyTo(
  locale: string,
  eventSlug: string,
  replyToId: string,
  _formData: FormData,
) {
  await getClient().mutate({
    mutation: deleteMessageReplyToMutation,
    variables: {
      input: {
        eventSlug,
        replyToId,
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-preferences`);
}
