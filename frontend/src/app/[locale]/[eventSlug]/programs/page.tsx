import { redirect } from "next/navigation";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export default function ProgramsRedirectPage({ params }: Props) {
  const { locale, eventSlug } = params;
  redirect(`/${eventSlug}/program`);
}
