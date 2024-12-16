"use server";

import { revalidatePath } from "next/cache";

export async function updateQuota(
  locale: string,
  eventSlug: string,
  quotaId: string,
  formData: FormData,
) {
  console.log("updateQuota", locale, eventSlug, quotaId, formData);
  revalidatePath(`/${locale}/${eventSlug}/quotas/${quotaId}`);
}
