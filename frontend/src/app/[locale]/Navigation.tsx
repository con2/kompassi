import Link from "next/link";
import { getServerSession } from "next-auth/next";

import NavigationMenus from "./NavigationMenus";
import { authOptions } from "@/auth";
import { SupportedLanguage, getTranslations } from "@/translations";

interface NavigationProps {
  locale: SupportedLanguage;
}

export default async function Navigation({ locale }: NavigationProps) {
  const translations = getTranslations(locale);
  const session = await getServerSession(authOptions);

  const messages = {
    LanguageSwitcher: translations.LanguageSwitcher,
    UserMenu: translations.UserMenu,
  };

  // NOTE: As of Bootstrap 5.3, the data-bs-theme attribute is preferred
  // over the deprecated .navbar-dark class. There is a complication with
  // the darkness/lightness of navbar menus: see comment in NavigationMenus.tsx.

  return (
    <div className="navbar bg-primary navbar-expand" data-bs-theme="dark">
      <div className="container-fluid">
        <Link href="/" className="navbar-brand">
          {translations.Brand.appName}
        </Link>
        {/* key: force remount when language changed to fix A->B->A transition */}
        <NavigationMenus
          key={locale}
          session={session}
          locale={locale}
          messages={messages}
        />
      </div>
    </div>
  );
}
