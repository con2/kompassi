import { getTranslations, toSupportedLanguage } from "@/translations";
import Navigation from "@/app/[locale]/Navigation";
import "./globals.scss";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Kompassi",
  description: "Event Management System",
};

interface RootLayoutProps {
  children: React.ReactNode;
  params: {
    locale: string;
  };
}

export default function RootLayout({
  children,
  params: { locale },
}: RootLayoutProps) {
  const supportedLanguage = toSupportedLanguage(locale);
  const translations = getTranslations(locale);

  return (
    <html lang={supportedLanguage}>
      <body>
        <Navigation locale={supportedLanguage} />
        {children}
      </body>
    </html>
  );
}
