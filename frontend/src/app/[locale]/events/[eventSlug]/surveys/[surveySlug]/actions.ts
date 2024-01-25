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

const fromEntriesWithMultiValues = (entries: [string, any][]) => {
  const map = new Map<string, any>();
  for (const [key, value] of entries) {
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
  return Object.fromEntries(map);
};

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  const client = getClient();
  const uploadFile = async (file: File): Promise<string> => {
    const filename = `${eventSlug}/survey-response-files/${surveySlug}/${file.name}`;
    const input = { filename, fileType: file.type };
    const init = await client.mutate({
      mutation: initFileUploadMutation,
      variables: { input },
    });
    const { uploadUrl, fileUrl } = init.data?.initFileUpload ?? {};
    if (!uploadUrl || !fileUrl)
      throw new Error("Failed to initialize file upload");

    await fetch(uploadUrl, { method: "PUT", body: file });
    return fileUrl;
  };

  const formEntries = Array.from(formData.entries());
  const fileUploadPromises = formEntries.map(
    async ([key, value]): Promise<[string, any]> => {
      if (!(value instanceof File)) return [key, value];
      // undefined removes the entry from the object
      if (value.size === 0) return [key, undefined];

      const fileUrl = await uploadFile(value);
      return [key, fileUrl];
    },
  );
  const withFileUrls = await Promise.all(fileUploadPromises);

  const input = {
    locale,
    eventSlug,
    surveySlug,
    formData: fromEntriesWithMultiValues(withFileUrls),
  };
  await client.mutate({
    mutation: createSurveyResponseMutation,
    variables: { input },
  });
  revalidatePath(`/events/${eventSlug}/surveys/${surveySlug}/responses`);
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
