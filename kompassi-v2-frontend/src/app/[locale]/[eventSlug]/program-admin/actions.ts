"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const mutation = graphql(`
  mutation CreateProgram($input: CreateProgramInput!) {
    createProgram(input: $input) {
      program {
        slug
      }
    }
  }
`);

export async function createProgram(
  locale: string,
  eventSlug: string,
  formData: FormData,
) {
  let slug: string;

  try {
    const { data, errors } = await getClient().mutate({
      mutation,
      variables: {
        input: {
          eventSlug,
          formData: Object.fromEntries(formData.entries()),
        },
      },
    });

    if (errors || !data?.createProgram?.program) {
      console.error("GraphQL error creating program:", errors);
      return void redirect(
        `/${eventSlug}/program-admin?error=failedToCreateProgram`,
      );
    }

    slug = data.createProgram.program.slug;
  } catch (error) {
    console.error("Exception occurred creating program:", error);
    return void redirect(
      `/${eventSlug}/program-admin?error=failedToCreateProgram`,
    );
  }

  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${slug}`);
  return void redirect(`/${eventSlug}/program-admin/${slug}`);
}
