import { redirect } from "next/navigation";

interface ProgrammeRedirectProps {
  params: {
    locale: string;
    eventSlug: string;
    path: string[];
  };
}

/**
 * Redirect programme -> program
 */
export default function ProgrammeRedirect({ params }: ProgrammeRedirectProps) {
  const { locale, eventSlug, path } = params;
  return void redirect(
    `/${locale}/events/${eventSlug}/programs/${path.join("/")}`
  );
}
