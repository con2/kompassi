"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { ProgramOfferResolution } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation AcceptProgramOffer($input: AcceptProgramOfferInput!) {
    acceptProgramOffer(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function acceptProgramOffer(
  locale: string,
  eventSlug: string,
  responseId: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    responseId,
    formData: Object.fromEntries(formData.entries()),
  };

  const { data, errors } = await getClient().mutate({
    mutation,
    variables: {
      input,
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  const program = data?.acceptProgramOffer?.program;
  if (!program) {
    throw new Error("Program not found");
  }

  revalidatePath(`/${locale}/${eventSlug}/program-offers/${responseId}`);
  revalidatePath(`/${locale}/${eventSlug}/program-offers`);
  redirect(`/${eventSlug}/program-admin/${program.slug}`);
}

const cancelProgramOfferMutation = graphql(`
  mutation CancelProgramOffer($input: CancelProgramOfferInput!) {
    cancelProgramOffer(input: $input) {
      responseId
    }
  }
`);

export async function cancelProgramOffer(
  locale: string,
  eventSlug: string,
  responseId: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    responseId,
    resolution: formData.get("resolution") as ProgramOfferResolution,
  };

  const { data, errors } = await getClient().mutate({
    mutation: cancelProgramOfferMutation,
    variables: {
      input,
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  const cancelledResponseId = data?.cancelProgramOffer?.responseId;
  if (!cancelledResponseId) {
    throw new Error("Backend did not return a response ID");
  }

  revalidatePath(
    `/${locale}/${eventSlug}/program-offers/${cancelledResponseId}`,
  );
  revalidatePath(`/${locale}/${eventSlug}/program-offers`);

  switch (input.resolution) {
    case ProgramOfferResolution.Cancel:
      redirect(
        `/${eventSlug}/program-offers/${cancelledResponseId}?success=cancelled`,
      );

    case ProgramOfferResolution.Reject:
      redirect(
        `/${eventSlug}/program-offers/${cancelledResponseId}?success=rejected`,
      );

    case ProgramOfferResolution.Delete:
      redirect(`/${eventSlug}/program-offers?success=deleted`);

    default:
      const _exhaustiveCheck: never = input.resolution;
      throw new Error(
        `Unknown resolution type ${_exhaustiveCheck} should have been rejected by server (this shouldn't happen)`,
      );
  }
}
