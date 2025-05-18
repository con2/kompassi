"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const inviteProgramHostMutation = graphql(`
  mutation InviteProgramHost($input: InviteProgramHostInput!) {
    inviteProgramHost(input: $input) {
      invitation {
        id
      }
    }
  }
`);

export async function inviteProgramHost(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  const surveySlug = formData.get("surveySlug") as string;
  const email = formData.get("email") as string;
  const language = formData.get("language") as string;

  await getClient().mutate({
    mutation: inviteProgramHostMutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        surveySlug,
        email,
        language,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
}

const deleteProgramHostMutation = graphql(`
  mutation DeleteProgramHost($input: DeleteProgramHostInput!) {
    deleteProgramHost(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function deleteProgramHost(
  locale: string,
  eventSlug: string,
  programSlug: string,
  involvementId: string,
) {
  await getClient().mutate({
    mutation: deleteProgramHostMutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        involvementId,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
}
