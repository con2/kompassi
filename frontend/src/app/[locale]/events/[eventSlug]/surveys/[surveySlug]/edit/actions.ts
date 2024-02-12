"use server";

export async function addLanguageVersion(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log("addLanguageVersion", {
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  });
}

export async function updateSurvey(
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  // TODO stubb
  console.log("updateSurvey", {
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData),
  });
}
