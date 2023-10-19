// TODO: remove usePathname, make server component
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { Translations } from "@/translations/en";

interface NavigationProps {
  translations: Translations;
}

export default function Navigation({ translations }: NavigationProps) {
  const { otherLanguage } = translations.LanguageSelection;
  const pathname = usePathname();

  // implemented in ../middleware.ts
  const languageToggleUri = `/${otherLanguage.code}${pathname}`;

  return (
    <div className="navbar navbar-dark bg-primary navbar-expand-lg">
      <div className="container-fluid">
        <Link href="/" className="navbar-brand">
          {translations.Brand.appName}
        </Link>
        <div className="navbar-nav ms-auto">
          <a
            href={languageToggleUri}
            className="nav-link"
            lang={otherLanguage.code}
          >
            {otherLanguage.nameInOtherLanguage}
          </a>
        </div>
      </div>
    </div>
  );
}
