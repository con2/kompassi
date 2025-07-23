"use client";

import { useParams } from "next/navigation";
import { useEffect } from "react";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { defaultLanguage } from "@/translations";

// NOTE: Don't use getTranslations here, as it would bundle all the translations.
// This is a fallback, so it should be lightweight.
const translations = {
  en: {
    title: "Something went wrong!",
    message: "Please try again later.",
  },
  fi: {
    title: "Jotain meni pieleen!",
    message: "Yritä myöhemmin uudelleen.",
  },
  sv: {
    title: "Något gick fel!",
    message: "Försök igen senare.",
  },
};

interface Props {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error }: Props) {
  // Log the error to an error reporting service
  useEffect(() => {
    console.error(error);
  }, [error]);

  let locale: string;
  const { locale: paramLocale } = useParams();
  if (Array.isArray(paramLocale)) {
    locale = paramLocale[0] || defaultLanguage;
  } else if (typeof paramLocale === "string") {
    locale = paramLocale || defaultLanguage;
  } else {
    locale = defaultLanguage;
  }

  const { title, message } =
    (translations as Record<string, { title: string; message: string }>)[
      locale
    ] ?? translations.en;

  return (
    <ViewContainer>
      <ViewHeading>{title}</ViewHeading>
      <p>{message}</p>
    </ViewContainer>
  );
}
