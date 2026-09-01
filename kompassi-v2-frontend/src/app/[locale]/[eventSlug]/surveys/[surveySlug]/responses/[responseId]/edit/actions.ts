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
  basePath: string,
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

  revalidatePath(`/${locale}/${basePath}`);
  revalidatePath(`/${locale}/${basePath}/${editResponseId}`);
  return void redirect(`/${basePath}/${newResponseId}?success=responseEdited`);
}
