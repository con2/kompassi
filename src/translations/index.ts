/**
 * Typesafe translation magic.
 * Enforces all supported languages to have all the same translation keys as English.
 */

import { ReactNode } from "react";
import en from "./en";
import fi from "./fi";

export type Translations = typeof en;
export type SupportedLanguage = "en" | "fi";
export const supportedLanguages: readonly SupportedLanguage[] = [
  "en",
  "fi",
] as const;
const defaultLanguage: SupportedLanguage = "en";

function getLanguageFromLocalStorage() {
  return localStorage.getItem("language");
}

export function setLanguage(language: string) {
  localStorage.setItem("language", language);
  location.reload();
}

function isSupportedLanguage(language: string): language is SupportedLanguage {
  return (supportedLanguages as string[]).includes(language);
}

function detectLanguage(): SupportedLanguage {
  const language =
    (global.localStorage && getLanguageFromLocalStorage()) ||
    (typeof navigator !== "undefined" && (navigator.languages || [navigator.language])[0]) ||
    defaultLanguage;

  if (!isSupportedLanguage(language)) {
    return defaultLanguage;
  }

  return language;
}

const languages = { en, fi };
export const detectedLanguage = detectLanguage();

const translations: Translations =
  (languages as any)[detectedLanguage] || languages[defaultLanguage];

export type TranslationKeyFunction<LocalTranslations = Translations> = (
  r: LocalTranslations
) => ReactNode;
export type TranslationFunction<LocalTranslations = Translations> = (
  fn: TranslationKeyFunction<LocalTranslations>
) => ReactNode;

export type HigherOrderTranslationKeyFunction<LocalTranslations> = (
  r: Translations
) => LocalTranslations;

export function t(fn: TranslationKeyFunction<Translations>) {
  return fn(translations);
}

export function T<LocalTranslations>(
  fn: HigherOrderTranslationKeyFunction<LocalTranslations>
) {
  return (gn: TranslationKeyFunction<LocalTranslations>) =>
    gn(fn(translations));
}
