import type { Metadata } from "next";

import Navigation from "../../components/navigation/Navigation";
import { toSupportedLanguage } from "@/translations";

import "./globals.scss";

export const metadata: Metadata = {
  title: "Kompassi",
  description: "Event Management System",
};

interface Props {
  children: React.ReactNode;
  params: {
    locale: string;
  };
}

export default function RootLayout({ children, params: { locale } }: Props) {
  const supportedLanguage = toSupportedLanguage(locale);

  // TODO implement bootstrap dark mode toggle (<html data-bs-theme="dark">)
  return (
    <html lang={supportedLanguage}>
      <body>
        <Navigation locale={supportedLanguage} />
        {children}
      </body>
    </html>
  );
}
