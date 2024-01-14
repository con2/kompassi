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

  return (
    <div className="navbar navbar-dark bg-primary navbar-expand-lg">
      <div className="container-fluid">
        <Link href="/" className="navbar-brand">
          {translations.Brand.appName}
        </Link>
        <NavigationMenus
          session={session}
          locale={locale}
          messages={messages}
        />
      </div>
    </div>
  );
}
