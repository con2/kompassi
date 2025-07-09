"use server";

import { revalidatePath } from "next/cache";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const generateKeyPairQuery = graphql(`
  mutation GenerateKeyPair($password: String!) {
    generateKeyPair(password: $password) {
      id
    }
  }
`);

export async function generateKeyPair(locale: string, formData: FormData) {
  const client = getClient();
  const password = formData.get("password") as string | null;
  if (!password) {
    throw new Error("Password is required");
  }

  await client.mutate({
    mutation: generateKeyPairQuery,
    variables: {
      password,
    },
  });

  revalidatePath(`/${locale}/profile/keys`);
}

const revokeKeyPairQuery = graphql(`
  mutation RevokeKeyPair($id: String!) {
    revokeKeyPair(id: $id) {
      id
    }
  }
`);

export async function revokeKeyPair(
  locale: string,
  id: string,
  _formData: FormData,
) {
  const client = getClient();
  await client.mutate({
    mutation: revokeKeyPairQuery,
    variables: {
      id,
    },
  });

  revalidatePath(`/${locale}/profile/keys`);
}
