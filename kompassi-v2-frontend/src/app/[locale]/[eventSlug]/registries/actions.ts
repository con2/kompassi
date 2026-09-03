"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation CreateRegistry($input: CreateRegistryInput!) {
    createRegistry(input: $input) {
      registry {
        slug
      }
    }
  }
`);

export async function createRegistry(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  const result = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        formData: Object.fromEntries(formData),
      },
    },
  });

  revalidatePath(`/${locale}/${eventSlug}/registries`);

  const newRegistrySlug = result.data?.createRegistry?.registry?.slug;
  redirect(`/${eventSlug}/registries/${newRegistrySlug ?? ""}`);
}
