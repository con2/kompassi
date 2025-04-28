"use server";

export async function updateProgramFormDefaultDimensions(
  locale: string,
  eventSlug: string,
  surveySlug: string,
  formData: FormData,
) {
  console.log("updateProgramFormDefaultDimensions", {
    locale,
    eventSlug,
    surveySlug,
    formData: Object.fromEntries(formData.entries()),
  });
}
