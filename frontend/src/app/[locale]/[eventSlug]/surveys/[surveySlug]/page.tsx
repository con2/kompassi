import { redirect } from "next/navigation";

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    surveySlug: string;
  }>;
}

export default async function SurveyRedirectPage(props: Props): Promise<never> {
  const params = await props.params;
  const { eventSlug, surveySlug } = params;
  redirect(`/${eventSlug}/${surveySlug}`);
}

export const generateMetadata = SurveyRedirectPage;
