import Link from "next/link";
import { getServerSession } from "next-auth/next";

import { authOptions } from "@/auth";
import { SupportedLanguage, getTranslations } from "@/translations";
import LanguageSwitcher from "./LanguageSwitcher";
import UserMenu from "./UserMenu";

interface NavigationProps {
  locale: SupportedLanguage;
}

export default async function Navigation({ locale }: NavigationProps) {
  const translations = getTranslations(locale);
  const session = await getServerSession(authOptions);

  return (
    <div className="navbar navbar-dark bg-primary navbar-expand-lg">
      <div className="container-fluid">
        <Link href="/" className="navbar-brand">
          {translations.Brand.appName}
        </Link>
        <div className="navbar-nav ms-auto">
          <LanguageSwitcher otherLanguage={translations.LanguageSelection.otherLanguage} />
          <UserMenu session={session} translations={translations.Navigation} />
        </div>
      </div>
    </div>
  );
}
