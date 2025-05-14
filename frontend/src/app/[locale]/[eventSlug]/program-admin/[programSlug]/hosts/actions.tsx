"use server";

export async function inviteProgramHost(
  locale: string,
  eventSlug: string,
  programSlug: string,
  formData: FormData,
) {
  console.log("inviteProgramHost", {
    locale,
    eventSlug,
    programSlug,
    email: "" + formData.get("email"),
  });
}

export async function removeProgramHost(
  locale: string,
  eventSlug: string,
  programSlug: string,
  involvementId: string,
) {
  console.log("removeProgramHost", {
    locale,
    eventSlug,
    programSlug,
    involvementId,
  });
}
