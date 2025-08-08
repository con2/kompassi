"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { decodeBoolean } from "@/helpers/decodeBoolean";
import { PutUniverseAnnotationAction } from "@/__generated__/graphql";

const universeSlug = "program";

const mutation = graphql(`
  mutation PutEventAnnotation($input: PutUniverseAnnotationInput!) {
    putUniverseAnnotation(input: $input) {
      universeAnnotation {
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
    formData.get("action") === PutUniverseAnnotationAction.SaveAndRefresh
      ? PutUniverseAnnotationAction.SaveAndRefresh
      : PutUniverseAnnotationAction.SaveWithoutRefresh;

  const isActive = annotationSlug.startsWith("internal:")
    ? true
    : decodeBoolean((formData.get("isActive") as string | null) || "false");

  const formFields = ((formData.get("formFields") as string | null) || "")
    .split("\n")
    .map((field) => field.trim())
    .filter(Boolean);

  const input = {
    scopeSlug: eventSlug,
    universeSlug,
    annotationSlug,
    isActive,
    formFields,
    action,
  };

  await getClient().mutate({
    mutation,
    variables: { input },
  });

  revalidatePath(`/${eventSlug}/program-annotations`);
}
