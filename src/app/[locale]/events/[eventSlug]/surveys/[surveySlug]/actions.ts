"use server";

import { redirect } from "next/navigation";

export async function submit(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData
) {
  console.log({
    locale,
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  });
  return void redirect(`/events/${eventSlug}/surveys/${surveySlug}/thanks`);
}
