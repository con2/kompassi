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
  const { data, errors } = await getClient().mutate({
    mutation,
    variables: {
      input: {
        eventSlug,
        formData: Object.fromEntries(formData.entries()),
      },
    },
  });

  if (errors) {
    throw new Error(errors[0].message);
  }

  if (!data?.createProgram?.program) {
    throw new Error("Program not created");
  }

  const { slug } = data.createProgram.program;

  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin/${slug}`);
  redirect(`/${eventSlug}/program-admin/${slug}`);
}
