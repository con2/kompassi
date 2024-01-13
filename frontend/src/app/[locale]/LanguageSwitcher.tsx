"use client";

import { usePathname } from "next/navigation";
import { supportedLanguages } from "@/translations";
import type { Translations } from "@/translations/en";

interface LanguageSwitcherProps {
  otherLanguage: Translations["LanguageSelection"]["otherLanguage"];
}

export default function LanguageSwitcher({ otherLanguage }: LanguageSwitcherProps) {
  let pathname = usePathname();

  // Remove the language prefix from the pathname
  // If we were using <Link>, Next.js would handle this for us
  // But that also sometimes preloads the link, causing a language change
  for (const supportedLanguage of supportedLanguages) {
    if (pathname === `/${supportedLanguage}` || pathname.startsWith(`/${supportedLanguage}/`)) {
      pathname = pathname.slice(supportedLanguage.length + 1);
      break;
    }
  }

  // implemented in ../middleware.ts
  const languageToggleUri = `/${otherLanguage.code}${pathname}`;

  return (
    <a href={languageToggleUri} className="nav-link" lang={otherLanguage.code}>
      {otherLanguage.nameInOtherLanguage}
    </a>
  );
}
