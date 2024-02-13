"use server";

export async function createSurvey(eventSlug: string, formData: FormData) {
  // TODO stubb
  console.log("createSurvey", {
    eventSlug,
    formData: Object.fromEntries(formData),
  });
}
