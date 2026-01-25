"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";

const createProgramFormMutation = graphql(`
  mutation CreateProgramForm($input: CreateProgramFormInput!) {
    createProgramForm(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function createProgramForm(eventSlug: string, formData: FormData) {
  const surveySlug = formData.get("slug")!.toString();
  const purpose = formData.get("purpose")!.toString() as SurveyPurpose;
  const copyFrom = formData.get("copyFrom")?.toString() || null;

  await getClient().mutate({
    mutation: createProgramFormMutation,
    variables: { input: { eventSlug, surveySlug, purpose, copyFrom } },
  });

  revalidatePath(`/${eventSlug}/program-forms`);
  redirect(`/${eventSlug}/program-forms/${surveySlug}/edit`);
}
