"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createProgramFormMutation = graphql(`
  mutation CreateProgramForm($input: CreateSurveyInput!) {
    createProgramForm(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function createProgramForm(eventSlug: string, formData: FormData) {
  const surveySlug = formData.get("slug")!.toString();

  await getClient().mutate({
    mutation: createProgramFormMutation,
    variables: { input: { eventSlug, surveySlug } },
  });

  revalidatePath(`/${eventSlug}/program-forms`);
  redirect(`/${eventSlug}/program-forms/${surveySlug}/edit`);
}
