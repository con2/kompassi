import { getTranslations, toSupportedLanguage } from "@/translations";
import Navigation from "@/components/Navigation";
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
  const translations = getTranslations(locale);

  return (
    <html lang={toSupportedLanguage(locale)}>
      <body>
        <Navigation translations={translations} />
        {children}
      </body>
    </html>
  );
}
