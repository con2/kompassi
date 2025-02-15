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
  // The /EVENT-SLUG/program-forms/SURVEY-SLUG URL pattern has never been used for customer-facing views
  // (as opposed to /EVENT-SLUG/surveys/SURVEY-SLUG) so we can use it to redirect to editor.
  // We still keep the /edit for parity with survey editor.
  redirect(`/${eventSlug}/${surveySlug}/edit`);
}

export const generateMetadata = ProgramFormRedirectPage;
