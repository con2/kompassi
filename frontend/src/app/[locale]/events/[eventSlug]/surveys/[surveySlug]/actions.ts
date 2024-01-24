"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const createSurveyResponseMutation = graphql(`
  mutation CreateSurveyResponse($input: CreateSurveyResponseInput!) {
    createSurveyResponse(input: $input) {
      response {
        id
      }
    }
  }
`);

const initFileUploadMutation = graphql(`
  mutation InitFileUploadMutation($input: InitFileUploadInput!) {
    initFileUpload(input: $input) {
      uploadUrl
      fileUrl
    }
  }
`);

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const client = getClient();

  for (const [key, value] of formData.entries()) {
    if (!(value instanceof File)) continue;

    const filename = `${eventSlug}/survey-response-files/${surveySlug}/${value.name}`;
    const input = { filename, fileType: value.type };
    const init = await client.mutate({
      mutation: initFileUploadMutation,
      variables: { input },
    });
    const { uploadUrl, fileUrl } = init.data?.initFileUpload ?? {};
    if (!uploadUrl || !fileUrl)
      throw new Error("Failed to initialize file upload");

    await fetch(uploadUrl, {
      method: "PUT",
      body: value,
    });
    formData.set(key, fileUrl);
  }

  const input = {
    locale,
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  };
  await client.mutate({
    mutation: createSurveyResponseMutation,
    variables: { input },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}/responses`);
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
