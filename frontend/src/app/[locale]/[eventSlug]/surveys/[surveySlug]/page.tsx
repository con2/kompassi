import { redirect } from "next/navigation";

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export default function SurveyRedirectPage({ params }: Props): never {
  const { eventSlug, surveySlug } = params;
  redirect(`/${eventSlug}/${surveySlug}`);
}

export const generateMetadata = SurveyRedirectPage;
