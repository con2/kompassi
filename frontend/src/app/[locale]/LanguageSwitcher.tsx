"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useReducer } from "react";

import type { Translations } from "@/translations/en";

interface Props {
  locale: string;
  messages: Translations["LanguageSwitcher"];
}

export default function LanguageSwitcher({ locale, messages }: Props) {
  const [isOpen, toggleOpen] = useReducer((isOpen) => !isOpen, false);
  const { supportedLanguages } = messages;
  let pathname = usePathname();

  // Remove the language prefix from the pathname
  // If we were using <Link>, Next.js would handle this for us
  // But that also sometimes preloads the link, causing a language change
  for (const supportedLanguage of Object.keys(supportedLanguages)) {
    if (
      pathname === `/${supportedLanguage}` ||
      pathname.startsWith(`/${supportedLanguage}/`)
    ) {
      pathname = pathname.slice(supportedLanguage.length + 1);
      break;
    }
  }

  return (
    <div className="nav-item dropdown">
      <button
        className="nav-link btn btn-link dropdown-toggle"
        id="user-menu"
        role="button"
        aria-expanded={isOpen}
        onClick={toggleOpen}
      >
        {locale.toUpperCase()}
      </button>
      <ul
        className={`dropdown-menu dropdown-menu-end ${isOpen ? "show" : ""}`}
        aria-labelledby="user-menu"
      >
        {Object.entries(supportedLanguages).map(([code, name]) => (
          <li key={code}>
            <Link
              href={`/${code}${pathname}`}
              className={`dropdown-item ${code === locale ? "active" : ""}`}
              onClick={toggleOpen}
            >
              {name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
