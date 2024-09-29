import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProgramFeedbackQuery($eventSlug: String!, $programSlug: String!) {
    event(slug: $eventSlug) {
      name
      program {
        program(slug: $programSlug) {
          title
          isAcceptingFeedback
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    programSlug: string;
  };
}

export const revalidate = 5;

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, programSlug },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.feedback.thankYou.title,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramFeedbackPage({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.feedback;

  return (
    <ViewContainer>
      <Link
        className="link-subtle"
        href={`/${eventSlug}/programs/${programSlug}`}
      >
        &lt; {t.actions.returnToProgram}
      </Link>

      <ViewHeading>{t.thankYou.title}</ViewHeading>

      <p>{t.thankYou.description}</p>
    </ViewContainer>
  );
}
