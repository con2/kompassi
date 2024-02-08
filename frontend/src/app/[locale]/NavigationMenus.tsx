"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Session } from "next-auth";
import { signIn, signOut } from "next-auth/react";
import { useState } from "react";

import type { Translations } from "@/translations/en";

interface Props {
  session: Session | null;
  locale: string;
  messages: {
    LanguageSwitcher: Translations["LanguageSwitcher"];
    UserMenu: Translations["UserMenu"];
  };
}

type OpenMenu = "none" | "user" | "language";

export default function NavigationMenus({ session, locale, messages }: Props) {
  const [openMenu, setOpenMenu] = useState<OpenMenu>("none");

  const isLanguageMenuOpen = openMenu === "language";
  const isUserMenuOpen = openMenu === "user";

  const toggleLanguageMenu = () => {
    setOpenMenu((openMenu) => (openMenu === "language" ? "none" : "language"));
  };

  const toggleUserMenu = () => {
    setOpenMenu((openMenu) => (openMenu === "user" ? "none" : "user"));
  };

  const { switchTo: supportedLanguages } = messages.LanguageSwitcher;
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

  // TODO: Remove hard-coded data-bs-theme when dark mode support is implemented
  // There's a catch: The navbar is dark also in light mode, but the menus should
  // follow the theme. So we may need to implement some kind of useTheme hook.

  return (
    <div className="navbar-nav ms-auto">
      <div className="nav-item dropdown" data-bs-theme="light">
        <button
          className="nav-link btn btn-link dropdown-toggle"
          id="user-menu"
          role="button"
          aria-expanded={isLanguageMenuOpen}
          onClick={toggleLanguageMenu}
        >
          {locale.toUpperCase()}
        </button>
        <ul
          className={`dropdown-menu dropdown-menu-end ${
            isLanguageMenuOpen ? "show" : ""
          }`}
          aria-labelledby="user-menu"
        >
          {Object.entries(supportedLanguages).map(([code, name]) => (
            <li key={code}>
              <Link
                href={`/${code}${pathname}`}
                className={`dropdown-item ${code === locale ? "active" : ""}`}
                onClick={toggleLanguageMenu}
              >
                {name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
      {session?.user ? (
        <div className="nav-item dropdown" data-bs-theme="light">
          <button
            className="nav-link btn btn-link dropdown-toggle"
            id="user-menu"
            role="button"
            aria-expanded={isUserMenuOpen}
            onClick={toggleUserMenu}
          >
            {session.user.name}
          </button>
          <ul
            className={`dropdown-menu dropdown-menu-end ${
              isUserMenuOpen ? "show" : ""
            }`}
            aria-labelledby="user-menu"
          >
            <li>
              <Link
                className="dropdown-item"
                href={`/profile/responses`}
                onClick={toggleUserMenu}
              >
                {messages.UserMenu.responses}
              </Link>
            </li>
            <li>
              <hr className="dropdown-divider" />
            </li>
            <li>
              <button className="dropdown-item" onClick={() => signOut()}>
                {messages.UserMenu.signOut}
              </button>
            </li>
          </ul>
        </div>
      ) : (
        <button
          onClick={() => signIn("kompassi")}
          className="nav-link btn btn-link"
        >
          {messages.UserMenu.signIn}…
        </button>
      )}
    </div>
  );
}
