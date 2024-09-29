"use server";

import { redirect } from "next/navigation";

export async function submit(
  locale: string,
  eventSlug: string,
  formSlug: string,
  formData: FormData,
) {
  console.log({
    locale,
    eventSlug,
    formSlug,
    formData: Object.fromEntries(formData),
  });
  return void redirect(`/events/${eventSlug}/programs/new`);
}
