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

const fromEntriesWithMultiValues = (entries: [string, string | string[]][]) => {
  const map = new Map<string, string | string[]>();
  for (const [key, value] of entries) {
    const existing = map.get(key);
    if (existing) {
      if (Array.isArray(existing) && Array.isArray(value)) {
        // FileUpload with multiple files
        map.set(key, [...existing, ...value]);
      } else {
        throw new Error(`Duplicate key that is not a FileUpload: ${key}`);
      }
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

      // FileUploads are string[] of URLs
      // All other fields are string
      return [key, [fileUrl]];
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
  revalidatePath(`/${eventSlug}/surveys/${surveySlug}/responses`);
  return void redirect(`/${eventSlug}/surveys/${surveySlug}/thanks`);
}
