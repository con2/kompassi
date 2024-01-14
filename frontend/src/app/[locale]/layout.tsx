import type { Metadata } from "next";

import Navigation from "./Navigation";
import { toSupportedLanguage } from "@/translations";

import "./globals.scss";

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

  return (
    <html lang={supportedLanguage}>
      <body>
        <Navigation locale={supportedLanguage} />
        {children}
      </body>
    </html>
  );
}
