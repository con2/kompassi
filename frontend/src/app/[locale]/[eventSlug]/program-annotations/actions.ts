"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { PutEventAnnotationAction } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { decodeBoolean } from "@/helpers/decodeBoolean";

const mutation = graphql(`
  mutation PutEventAnnotation($input: PutEventAnnotationInput!) {
    putEventAnnotation(input: $input) {
      eventAnnotation {
        annotation {
          slug
        }
      }
    }
  }
`);

export async function putEventAnnotation(
  eventSlug: string,
  annotationSlug: string,
  formData: FormData,
) {
  const action =
    formData.get("action") === PutEventAnnotationAction.SaveAndRefresh
      ? PutEventAnnotationAction.SaveAndRefresh
      : PutEventAnnotationAction.SaveWithoutRefresh;

  const isActive = annotationSlug.startsWith("internal:")
    ? true
    : decodeBoolean((formData.get("isActive") as string | null) || "false");

  const programFormFields = (
    (formData.get("programFormFields") as string | null) || ""
  )
    .split("\n")
    .map((field) => field.trim())
    .filter(Boolean);

  const input = {
    eventSlug,
    annotationSlug,
    isActive,
    programFormFields,
    action,
  };

  await getClient().mutate({
    mutation,
    variables: { input },
  });

  revalidatePath(`/${eventSlug}/program-annotations`);
}
