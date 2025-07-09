"use client";

import { useParams } from "next/navigation";
import { useEffect } from "react";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";

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

  let { locale } = useParams();
  if (Array.isArray(locale)) {
    locale = locale[0];
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
