import { redirect } from "next/navigation";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export default function ProgramFormRedirectPage({ params }: Props): never {
  const { eventSlug, surveySlug } = params;
  redirect(`/${eventSlug}/${surveySlug}`);
}

export const generateMetadata = ProgramFormRedirectPage;
