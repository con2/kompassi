"use server";

export async function markAsFavorite({
  eventSlug,
  programSlug,
}: {
  eventSlug: string;
  programSlug: string;
}) {
  // TODO stubb
  console.log("markAsFavorite", eventSlug, programSlug);
}

export async function unmarkAsFavorite({
  eventSlug,
  programSlug,
}: {
  eventSlug: string;
  programSlug: string;
}) {
  // TODO stubb
  console.log("unmarkAsFavorite", eventSlug, programSlug);
}
