"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { ProgramItemResolution } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation UpdateProgramBasicInfo($input: UpdateProgramInput!) {
    updateProgram(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function updateProgramBasicInfo(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/program-admin/${programSlug}`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
}

const cancelProgramItemMutation = graphql(`
  mutation CancelProgramItem($input: CancelProgramInput!) {
    cancelProgram(input: $input) {
      responseId
    }
  }
`);

export async function cancelProgramItemWithResolutionForm(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  const resolution = formData.get("resolution") as ProgramItemResolution;
  return cancelProgramItem(locale, eventSlug, programSlug, resolution);
}

export async function cancelProgramItem(
  locale: string,
  eventSlug: string,
  programSlug: string,
  resolution: ProgramItemResolution,
) {
  const input = {
    eventSlug,
    programSlug,
    resolution,
  };

  const { data, errors } = await getClient().mutate({
    mutation: cancelProgramItemMutation,
    variables: {
      input,
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  revalidatePath(`/${locale}/${eventSlug}/program-admin`);

  const cancelledResponseId = data?.cancelProgram?.responseId;
  if (!cancelledResponseId) {
    // The program was not created from a program offer.
    redirect(`/${eventSlug}/program-admin?success=removed`);
  }

  revalidatePath(
    `/${locale}/${eventSlug}/program-offers/${cancelledResponseId}`,
  );

  switch (input.resolution) {
    case ProgramItemResolution.Cancel:
    case ProgramItemResolution.CancelAndHide:
      redirect(
        `/${eventSlug}/program-offers/${cancelledResponseId}?success=spawnCancelled`,
      );

    case ProgramItemResolution.Delete:
      redirect(`/${eventSlug}/program-offers?success=spawnDeleted`);

    default:
      const _exhaustiveCheck: never = input.resolution;
      throw new Error(
        `Unknown resolution type ${_exhaustiveCheck} should have been rejected by server (this shouldn't happen)`,
      );
  }
}

const restoreProgramItemMutation = graphql(`
  mutation RestoreProgramItem($input: RestoreProgramInput!) {
    restoreProgram(input: $input) {
      programSlug
    }
  }
`);
export async function restoreProgramItem(
  locale: string,
  eventSlug: string,
  programSlug: string,
) {
  const input = {
    eventSlug,
    programSlug,
  };

  const { data, errors } = await getClient().mutate({
    mutation: restoreProgramItemMutation,
    variables: {
      input,
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  const restoredProgramSlug = data?.restoreProgram?.programSlug;
  if (!restoredProgramSlug) {
    throw new Error(
      "The program was not restored successfully. Please try again.",
    );
  }

  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
  revalidatePath(
    `/${locale}/${eventSlug}/program-admin/${restoredProgramSlug}`,
  );
  redirect(
    `/${eventSlug}/program-admin/${programSlug}?success=programRestored`,
  );
}
