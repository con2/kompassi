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

const formDataToObject = (formData: FormData) => {
  const map = new Map<string, any>();
  for (const [key, value] of formData.entries()) {
    if (map.has(key)) {
      const existing = map.get(key);
      if (!Array.isArray(existing)) {
        map.set(key, [existing]);
      }
      map.get(key).push(value);
    } else {
      map.set(key, value);
    }
  }
  return Object.fromEntries(map.entries());
};

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const client = getClient();

  const entries = Array.from(formData.entries());
  // Remove files from form data
  for (const key of formData.keys()) {
    const value = formData.get(key);
    if (value instanceof File) formData.delete(key);
  }
  // Replace files with file URLs
  for (const [key, value] of entries) {
    if (!(value instanceof File)) continue;
    if (value.size === 0) continue;

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
    formData.append(key, fileUrl);
  }

  const input = {
    locale,
    eventSlug,
    surveySlug,
    formData: formDataToObject(formData),
  };
  await client.mutate({
    mutation: createSurveyResponseMutation,
    variables: { input },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}/responses`);
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
