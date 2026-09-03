"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const updateRegistryMutation = graphql(`
  mutation UpdateRegistry($input: UpdateRegistryInput!) {
    updateRegistry(input: $input) {
      registry {
        slug
      }
    }
  }
`);

export async function updateRegistry(
  locale: string,
  eventSlug: string,
  registrySlug: string,
  formData: FormData,
) {
  const input = {
    eventSlug,
    registrySlug,
    formData: Object.fromEntries(formData),
  };

  await getClient().mutate({
    mutation: updateRegistryMutation,
    variables: { input },
  });

  revalidatePath(`/${locale}/${eventSlug}/registries/${registrySlug}`);
}

const deleteRegistryMutation = graphql(`
  mutation DeleteRegistry($input: DeleteRegistryInput!) {
    deleteRegistry(input: $input) {
      slug
    }
  }
`);

export async function deleteRegistry(
  locale: string,
  eventSlug: string,
  registrySlug: string,
) {
  await getClient().mutate({
    mutation: deleteRegistryMutation,
    variables: {
      input: { eventSlug, registrySlug },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/registries`);
  redirect(`/${eventSlug}/registries`);
}
