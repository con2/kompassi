"use server";

export async function acceptProgramOffer(
  locale: string,
  eventSlug: string,
  responseId: string,
  formData: FormData,
) {
  console.log(
    "acceptProgramOffer",
    locale,
    eventSlug,
    responseId,
    Object.fromEntries(formData),
  );
}
