"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { buildScheduleItemForm } from "./ScheduleItemForm";
import { graphql } from "@/__generated__";
import { PutScheduleItemInput } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import processFormData from "@/components/forms/processFormData";

const putScheduleItemMutation = graphql(`
  mutation PutScheduleItem($input: PutScheduleItemInput!) {
    putScheduleItem(input: $input) {
      scheduleItem {
        slug
      }
    }
  }
`);

export async function putScheduleItem(
  locale: string,
  eventSlug: string,
  programSlug: string,
  scheduleItemSlug: string | null,
  formData: FormData,
) {
  const editingExisting = !!scheduleItemSlug;

  const fields = buildScheduleItemForm(
    eventSlug,
    editingExisting,
    "pass-through",
  );

  const scheduleItem = processFormData(
    fields,
    formData,
  ) as unknown as PutScheduleItemInput["scheduleItem"];

  if (editingExisting) {
    scheduleItem.slug = scheduleItemSlug;
  }

  const input = {
    eventSlug,
    programSlug,
    scheduleItem,
  };

  const client = getClient();

  const { data, errors } = await client.mutate({
    mutation: putScheduleItemMutation,
    variables: { input },
  });

  if (errors) {
    throw new Error(errors.map((e) => e.message).join(", "));
  }

  const action = editingExisting ? "updated" : "created";

  revalidatePath(`/${locale}/${eventSlug}/program`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
  revalidatePath(
    `/${locale}/${eventSlug}/program-admin/${programSlug}/schedule`,
  );
  redirect(
    `/${eventSlug}/program-admin/${programSlug}/schedule?success=${action}`,
  );
}

const deleteScheduleItemMutation = graphql(`
  mutation DeleteScheduleItem($input: DeleteScheduleItemInput!) {
    deleteScheduleItem(input: $input) {
      slug
    }
  }
`);

export async function deleteScheduleItem(
  locale: string,
  eventSlug: string,
  programSlug: string,
  scheduleItemSlug: string,
) {
  const input = {
    eventSlug,
    programSlug,
    scheduleItemSlug,
  };

  const client = getClient();

  const { data, errors } = await client.mutate({
    mutation: deleteScheduleItemMutation,
    variables: { input },
  });

  if (errors) {
    throw new Error(errors.map((e) => e.message).join(", "));
  }

  revalidatePath(`/${locale}/${eventSlug}/program`);
  revalidatePath(`/${locale}/${eventSlug}/program-admin`);
  revalidatePath(
    `/${locale}/${eventSlug}/program-admin/${programSlug}/schedule`,
  );
  redirect(
    `/${eventSlug}/program-admin/${programSlug}/schedule?success=removed`,
  );
}
