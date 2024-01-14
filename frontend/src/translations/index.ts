/**
 * Typesafe translation magic.
 * Enforces all supported languages to have all the same translation keys as English.
 */

import type { Translations } from "./en";

import en from "./en";
import fi from "./fi";

export type SupportedLanguage = "en" | "fi";
export const supportedLanguages: readonly SupportedLanguage[] = [
  "en",
  "fi",
] as const;
export const defaultLanguage: SupportedLanguage = "en";
export const languages = { en, fi };

export function isSupportedLanguage(
  language?: string,
): language is SupportedLanguage {
  return (
    typeof language === "string" &&
    (supportedLanguages as string[]).includes(language)
  );
}

export function getTranslations(language: string): Translations {
  const supportedLanguage = isSupportedLanguage(language)
    ? language
    : defaultLanguage;
  return languages[supportedLanguage];
}

export function toSupportedLanguage(language: string) {
  return isSupportedLanguage(language) ? language : defaultLanguage;
}
