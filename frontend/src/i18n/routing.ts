import { defineRouting } from "next-intl/routing";
import { supportedLanguages, defaultLanguage } from "@/translations";

export const routing = defineRouting({
  locales: supportedLanguages,
  defaultLocale: defaultLanguage,
  localePrefix: "never",
});
