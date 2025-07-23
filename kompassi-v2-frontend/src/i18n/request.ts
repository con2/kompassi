import { getRequestConfig } from "next-intl/server";
import { defaultLanguage, toSupportedLanguage } from "@/translations";

export default getRequestConfig(async ({ requestLocale }) => {
  const locale = toSupportedLanguage((await requestLocale) ?? defaultLanguage);
  return {
    locale,
    messages: {},
  };
});
