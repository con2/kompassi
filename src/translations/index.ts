/**
 * Typesafe translation magic.
 * Enforces all supported languages to have all the same translation keys as English.
 */

import { ReactNode } from "react";
import en from "./en";
import fi from "./fi";

export type Translations = typeof en;

const languages = { en, fi };
const defaultLanguage = "en";
const detectedLanguage =
  (navigator.languages || [navigator.language])[0] || defaultLanguage;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
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
