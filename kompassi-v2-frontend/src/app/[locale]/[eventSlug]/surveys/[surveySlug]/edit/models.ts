export interface Survey {
  slug: string;
  title?: string | null;
  canRemove: boolean;
  canGrantAccess: boolean;
  languages: {
    language: string;
  }[];
  purpose: "DEFAULT" | "INVITE" | "FOLLOWUP";
}

/// Human-readable names of the language versions of a survey, eg. "Finnish, English"
export function getLanguageVersionNames(
  survey: Survey,
  supportedLanguages: Record<string, string>,
): string {
  return survey.languages
    .map(
      ({ language }) =>
        supportedLanguages[language.toLowerCase()] ?? language.toUpperCase(),
    )
    .join(", ");
}
