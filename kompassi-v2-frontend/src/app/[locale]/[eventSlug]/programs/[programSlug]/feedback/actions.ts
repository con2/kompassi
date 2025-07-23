"use server";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

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
  await getClient().mutate({
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
