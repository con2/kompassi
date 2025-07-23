"use server";

import { redirect } from "next/navigation";
import { uploadFiles } from "../../[surveySlug]/actions";
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
  surveySlug: string,
  invitationId: string,
  formData: FormData,
) {
  const client = getClient();
  await client.mutate({
    mutation,
    variables: {
      input: {
        locale,
        eventSlug,
        invitationId,
        formData: await uploadFiles(eventSlug, surveySlug, formData),
      },
    },
  });
  redirect(`/profile/program?message=invitation-accepted`);
}
