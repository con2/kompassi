"use server";

export async function updateForm(
  eventSlug: string,
  surveySlug: string,
  language: string,
  formData: FormData,
) {
  console.log("updateForm", {
    eventSlug,
    surveySlug,
    language,
    formData: Object.fromEntries(formData),
  });
}
