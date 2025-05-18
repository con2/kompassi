"use server";

import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation AcceptInvitation($input: AcceptInvitationInput!) {
    acceptInvitation(input: $input) {
      involvement {
        program {
          slug
        }
      }
    }
  }
`);

export async function acceptInvitation(
  locale: string,
  eventSlug: string,
  invitationId: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation,
    variables: { input: { locale, eventSlug, invitationId, formData } },
  });
  redirect(`/profile/program?message=invitation-accepted`);
}
