"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { annotationSlugs } from "./consts";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { updateProgramAnnotationsFromFormData } from "@/components/annotations/service";

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

const deleteInvitationMutation = graphql(`
  mutation DeleteInvitation($input: DeleteInvitationInput!) {
    deleteInvitation(input: $input) {
      invitation {
        id
      }
    }
  }
`);

export async function revokeInvitation(
  locale: string,
  eventSlug: string,
  programSlug: string,
  invitationId: string,
) {
  await getClient().mutate({
    mutation: deleteInvitationMutation,
    variables: {
      input: {
        eventSlug,
        invitationId,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
}

const resendInvitationMutation = graphql(`
  mutation ResendInvitation($input: ResendInvitationInput!) {
    resendInvitation(input: $input) {
      invitation {
        id
      }
    }
  }
`);

export async function resendInvitation(
  locale: string,
  eventSlug: string,
  programSlug: string,
  invitationId: string,
) {
  await getClient().mutate({
    mutation: resendInvitationMutation,
    variables: {
      input: {
        eventSlug,
        invitationId,
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
  redirect(
    `/${eventSlug}/program-admin/${programSlug}/hosts?resent=${invitationId}`,
  );
}

export async function overrideFormattedHosts(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  await updateProgramAnnotationsFromFormData(
    eventSlug,
    programSlug,
    formData,
    annotationSlugs,
  );

  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
}
