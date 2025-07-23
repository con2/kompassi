import Link from "next/link";
import { ReactNode } from "react";
import { isSupportedLanguage, SupportedLanguage } from "@/translations";
import en, { Translations } from "@/translations/en";
import fi from "@/translations/fi";
import sv from "@/translations/sv";

// NOTE SUPPORTED_LANGUAGES
// XXX ugly
const alsoAvailableIn: Record<
  SupportedLanguage,
  Translations["Survey"]["attributes"]["alsoAvailableInThisLanguage"]
> = {
  en: en.Survey.attributes.alsoAvailableInThisLanguage,
  fi: fi.Survey.attributes.alsoAvailableInThisLanguage,
  sv: sv.Survey.attributes.alsoAvailableInThisLanguage,
};

interface FormLanguage {
  language: string;
}

interface Props {
  /// The language the form is currently being displayed in.
  /// NOTE: May differ from the current locale (when form is not available in the current locale).
  language: string;
  /// The languages the form is available in.
  languages: FormLanguage[];
  /// Current path (eg. /tracon2025/offer-program).
  path: string;
}

export function AlsoAvailableInLanguage({ language, languages, path }: Props) {
  const otherLanguages: SupportedLanguage[] = languages
    .map((languageObj) => languageObj.language.toLowerCase())
    .filter((lang) => lang != language.toLowerCase())
    .filter(isSupportedLanguage);

  if (otherLanguages.length > 0) {
    return (
      <div className="alert alert-primary">
        {otherLanguages.map((lang) => {
          function LanguageLink({ children }: { children: ReactNode }) {
            return (
              <Link prefetch={false} href={`/${lang}${path}`} lang={lang}>
                {children}
              </Link>
            );
          }

          return (
            <div key={lang} lang={lang}>
              {alsoAvailableIn[lang](LanguageLink)}{" "}
            </div>
          );
        })}
      </div>
    );
  } else {
    return <></>;
  }
}
