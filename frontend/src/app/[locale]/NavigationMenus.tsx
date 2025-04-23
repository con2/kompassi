"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Session } from "next-auth";
import { signIn, signOut } from "next-auth/react";

import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";

import type { Translations } from "@/translations/en";

interface Props {
  session: Session | null;
  locale: string;
  messages: {
    LanguageSwitcher: Translations["LanguageSwitcher"];
    UserMenu: Translations["UserMenu"];
  };
}

interface ProfileLink {
  title: string;
  href: string;
}

type OpenMenu = "none" | "user" | "language";

export default function NavigationMenus({ session, locale, messages }: Props) {
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

  const links: ProfileLink[] = [
    { href: "/profile/orders", title: messages.UserMenu.tickets },
    { href: "/profile/responses", title: messages.UserMenu.responses },
    { href: "/profile/keys", title: messages.UserMenu.keys },
  ];

  return (
    <Nav className="navbar-nav ms-auto">
      <NavDropdown
        title={locale.toUpperCase()}
        id="kompassi-locale-menu"
        data-bs-theme="light"
      >
        {Object.entries(supportedLanguages).map(([code, name]) => (
          <NavDropdown.Item
            key={code}
            as={Link}
            href={`/${code}${pathname}`}
            active={code === locale}
            prefetch={false}
          >
            {name}
          </NavDropdown.Item>
        ))}
      </NavDropdown>
      {session?.user ? (
        <NavDropdown
          title={session.user.name}
          id="kompassi-user-menu"
          data-bs-theme="light"
          align="end"
        >
          {links.map(({ href, title }) => (
            <NavDropdown.Item key={href} as={Link} href={href}>
              {title}
            </NavDropdown.Item>
          ))}
          <NavDropdown.Divider />
          <NavDropdown.Item onClick={() => signOut()}>
            {messages.UserMenu.signOut}
          </NavDropdown.Item>
        </NavDropdown>
      ) : (
        <Nav.Link onClick={() => signIn("kompassi")}>
          {messages.UserMenu.signIn}…
        </Nav.Link>
      )}
    </Nav>
  );
}
