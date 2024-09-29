import Link from "next/link";
import { notFound } from "next/navigation";

import { createProgramFeedback } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
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
    viewTitle: translations.Program.feedback.viewTitle,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramFeedbackPage({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.feedback;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug },
  });
  const { event } = data;
  if (!event?.program?.program) {
    notFound();
  }

  const program = event.program.program;

  if (!program.isAcceptingFeedback) {
    return (
      <ViewContainer>
        <ViewHeading>{t.notAcceptingFeedback}</ViewHeading>
      </ViewContainer>
    );
  }

  const fields: Field[] = [
    {
      slug: "feedback",
      type: "MultiLineText",
      required: true,
      ...t.fields.feedback,
    },
    {
      slug: "kissa",
      type: "SingleLineText",
      required: true,
      ...t.fields.kissa,
    },
  ];

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${eventSlug}/program`}>
        &lt; {t.actions.returnToProgram}
      </Link>

      <ViewHeading>
        {program.title}
        <ViewHeading.Sub>{t.viewTitle}</ViewHeading.Sub>
      </ViewHeading>

      <form
        action={createProgramFeedback.bind(
          null,
          locale,
          eventSlug,
          programSlug,
        )}
      >
        <SchemaForm fields={fields} messages={translations.SchemaForm} />
        <SubmitButton>{t.actions.submit}</SubmitButton>
      </form>
      <p className="mt-3 text-muted">
        <small>
          <strong>{t.anonymity.title}: </strong>
          {t.anonymity.description}
        </small>
      </p>
    </ViewContainer>
  );
}
