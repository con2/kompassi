import { notFound } from "next/navigation";

import { SchemaForm } from "@/components/SchemaForm";
import { Field } from "@/components/SchemaForm/models";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import Link from "next/link";

const query = gql(`
  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      # this is only needed to check if there is exactly one program form
      # in which case the link back to form selection should not be shown
      offerForms {
        slug
      }

      offerForm(slug: $formSlug) {
        shortDescription(lang: $locale)
        form(lang: $locale) {
          title
          description
          fields
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

export const revalidate = 15;

export async function generateMetadata({ params }: NewProgramProps) {
  const { locale, eventSlug, formSlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, formSlug, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.offerForm?.form?.title} – Kompassi`,
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
  const { offerForms, offerForm } = event;
  if (!offerForm) {
    notFound();
  }
  const { form } = offerForm;
  const { title, description, fields: fieldsJson } = form!;
  const fields: Field[] = JSON.parse(fieldsJson);

  const showBackToProgramFormSelectionLink = offerForms?.length !== 1;

  return (
    <main className="container mt-4">
      {showBackToProgramFormSelectionLink && (
        <nav className="mb-0">
          <Link
            className="link-subtle"
            href={`/events/${eventSlug}/program/new`}
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
      <SchemaForm fields={fields} layout={"horizontal"} />
    </main>
  );
}
