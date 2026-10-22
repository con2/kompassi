interface ProfileWithId {
  id: string;
}

// The signed-in user is part of the key so that on a shared browser one
// person's unsent answers are never restored into another person's form.
function userPart(profile: ProfileWithId | null | undefined): string {
  return profile?.id ?? "anon";
}

export function surveyDraftKey(
  eventSlug: string,
  surveySlug: string,
  profile: ProfileWithId | null | undefined,
): string {
  return `survey:${eventSlug}/${surveySlug}:${userPart(profile)}`;
}

export function invitationDraftKey(
  invitationId: string,
  profile: ProfileWithId | null | undefined,
): string {
  return `invitation:${invitationId}:${userPart(profile)}`;
}

export function feedbackDraftKey(
  eventSlug: string,
  programSlug: string,
  profile: ProfileWithId | null | undefined,
): string {
  return `feedback:${eventSlug}/${programSlug}:${userPart(profile)}`;
}
