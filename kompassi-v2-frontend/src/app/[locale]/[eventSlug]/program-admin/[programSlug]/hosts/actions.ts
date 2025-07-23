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
  await getClient().mutate({
    mutation: inviteProgramHostMutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        formData: Object.fromEntries(formData.entries()),
      },
    },
  });
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
  redirect(`/${eventSlug}/program-admin/${programSlug}/hosts?success=invited`);
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
  redirect(`/${eventSlug}/program-admin/${programSlug}/hosts?success=deleted`);
}

const updateProgramHostDimensionsMutation = graphql(`
  mutation UpdateProgramHostDimensions(
    $input: UpdateInvolvementDimensionsInput!
  ) {
    updateInvolvementDimensions(input: $input) {
      involvement {
        program {
          slug
        }
      }
    }
  }
`);

export async function updateProgramHostDimensions(
  locale: string,
  eventSlug: string,
  involvementId: string,
  formData: FormData,
) {
  const { data, errors } = await getClient().mutate({
    mutation: updateProgramHostDimensionsMutation,
    variables: {
      input: {
        involvementId,
        eventSlug,
        formData: Object.fromEntries(formData.entries()),
      },
    },
  });

  const programSlug =
    data?.updateInvolvementDimensions?.involvement?.program?.slug;
  if (!programSlug) {
    throw new Error(
      "Failed to update program host dimensions: Program slug is missing.",
    );
  }

  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}/hosts`);
  redirect(`/${eventSlug}/program-admin/${programSlug}/hosts?success=updated`);
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
  redirect(`/${eventSlug}/program-admin/${programSlug}/hosts?success=revoked`);
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
  redirect(`/${eventSlug}/program-admin/${programSlug}/hosts?success=resent`);
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
