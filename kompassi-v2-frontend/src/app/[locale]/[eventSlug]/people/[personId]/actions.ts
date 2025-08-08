"use server";

export async function updateCombinedPerks(
  locale: string,
  eventSlug: string,
  personId: number,
  formData: FormData,
) {
  console.log({
    locale,
    eventSlug,
    personId,
    formData: Object.fromEntries(formData.entries()),
  });
}
