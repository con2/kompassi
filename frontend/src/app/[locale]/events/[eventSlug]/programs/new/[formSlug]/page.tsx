import Link from "next/link";
import { notFound } from "next/navigation";

import { submit } from "./actions";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { SchemaForm } from "@/components/SchemaForm";
import SubmitButton from "@/components/SchemaForm/SubmitButton";
import { getTranslations } from "@/translations";

const query = gql(`
  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name
      program {
        skipOfferFormSelection

        offerForm(slug: $formSlug) {
          form(lang: $locale) {
            title
            description
            fields
            layout
          }
        }
      }
    }
  }
`);

interface NewProgramProps {
  params: {
    locale: string;
    eventSlug: string;
    formSlug: string;
  };
}

export const revalidate = 5;

export async function generateMetadata({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, formSlug, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.program?.offerForm?.form?.title} – Kompassi`,
  };
}

export default async function NewProgramPage({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const t = getTranslations(locale).NewProgrammeView;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, formSlug, locale },
  });
  const { event } = data;
  if (!event) {
    notFound();
  }
  const offerForm = event.program?.offerForm;
  if (!offerForm) {
    notFound();
  }
  const skipOfferFormSelection = event.program?.skipOfferFormSelection ?? false;
  const { form } = offerForm;
  const { title, description, fields, layout } = form!;

  return (
    <main className="container mt-4">
      {skipOfferFormSelection || (
        <nav className="mb-0">
          <Link
            className="link-subtle"
            href={`/events/${eventSlug}/programs/new`}
          >
            &lt; {t.backToProgramFormSelection}
          </Link>
        </nav>
      )}
      <h1 className="mt-2 mb-4">
        {title}{" "}
        <span className="fs-5 text-muted">{t.forEvent(event.name)}</span>
      </h1>
      <p>{description}</p>
      <form action={submit.bind(null, locale, eventSlug, formSlug)}>
        <SchemaForm fields={fields} layout={layout} />
        <SubmitButton layout={layout}>{t.submit}</SubmitButton>
      </form>
    </main>
  );
}
