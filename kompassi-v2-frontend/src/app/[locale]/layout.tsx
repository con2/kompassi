import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { hasLocale } from "next-intl";

import { routing } from "@/i18n/routing";
import Navigation from "../../components/navigation/Navigation";

import "./globals.scss";

export const metadata: Metadata = {
  title: "Kompassi",
  description: "Event Management System",
};

interface Props {
  children: React.ReactNode;
  params: Promise<{
    locale: string;
  }>;
}

export default async function RootLayout(props: Props) {
  const params = await props.params;

  const { locale } = params;

  const { children } = props;

  if (!hasLocale(routing.locales, locale)) notFound();

  // TODO implement bootstrap dark mode toggle (<html data-bs-theme="dark">)
  return (
    <html lang={locale} data-scroll-behavior="smooth">
      <body>
        <Navigation locale={locale} />
        {children}
      </body>
    </html>
  );
}
