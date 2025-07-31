"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { uploadFiles } from "@/app/[locale]/[eventSlug]/[surveySlug]/actions";

const mutation = graphql(`
  mutation EditSurveyResponse($input: CreateSurveyResponseInput!) {
    createSurveyResponse(input: $input) {
      response {
        id
      }
    }
  }
`);

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  editResponseId: string,
  formData: FormData,
) {
  const client = getClient();
  const input = {
    locale,
    eventSlug,
    surveySlug,
    editResponseId,
    formData: await uploadFiles(eventSlug, surveySlug, formData),
  };

  const { data } = await client.mutate({
    mutation,
    variables: { input },
  });

  const newResponseId = data?.createSurveyResponse?.response?.id;
  if (!newResponseId) {
    throw new Error("Failed to create survey response");
  }

  revalidatePath(`/${locale}/${eventSlug}/surveys/${surveySlug}/responses`);
  revalidatePath(
    `/${locale}/${eventSlug}/surveys/${surveySlug}/responses/${editResponseId}`,
  );
  return void redirect(
    `/${eventSlug}/surveys/${surveySlug}/responses/${newResponseId}?success=responseEdited`,
  );
}
