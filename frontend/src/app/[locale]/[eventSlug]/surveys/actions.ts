"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createSurveyMutation = graphql(`
  mutation CreateSurvey($input: CreateSurveyInput!) {
    createSurvey(input: $input) {
      survey {
        slug
      }
    }
  }
`);

export async function createSurvey(eventSlug: string, formData: FormData) {
  const surveySlug = formData.get("slug")!.toString();
  const anonymity = formData.get("anonymity")!.toString();
  const copyFrom = formData.get("copyFrom")?.toString() ?? null;

  await getClient().mutate({
    mutation: createSurveyMutation,
    variables: {
      input: { eventSlug, surveySlug, anonymity: anonymity as any, copyFrom },
    },
  });

  revalidatePath(`/${eventSlug}/surveys`);
  redirect(`/${eventSlug}/surveys/${surveySlug}/edit`);
}
