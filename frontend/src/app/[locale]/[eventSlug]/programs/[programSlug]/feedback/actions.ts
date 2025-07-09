"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { FavoriteInput } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const createProgramFeedbackMutation = graphql(`
  mutation CreateFeedback($input: ProgramFeedbackInput!) {
    createProgramFeedback(input: $input) {
      success
    }
  }
`);

export async function createProgramFeedback(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  const data = await getClient().mutate({
    mutation: createProgramFeedbackMutation,
    variables: {
      input: {
        eventSlug,
        programSlug,
        feedback: formData.get("feedback")?.toString() ?? "",
        kissa: formData.get("kissa")?.toString() ?? "",
      },
    },
  });
  revalidatePath(`/${locale}}/${eventSlug}/programs/${programSlug}/feedback`);
  redirect(`/${eventSlug}/programs/${programSlug}/feedback/thanks`);
}
