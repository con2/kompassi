import { notFound } from "next/navigation";

import { SchemaForm } from "@/components/SchemaForm";
import { Field } from "@/components/SchemaForm/models";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";

const query = gql(`
  query ProgrammeExampleQuery($eventSlug:String!, $formSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

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
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, formSlug, locale },
  });
  const { event } = data;
  if (!event) {
    notFound();
  }
  const { offerForm } = event;
  if (!offerForm) {
    notFound();
  }
  const { form } = offerForm;
  const { title, description, fields: fieldsJson } = form!;
  const fields: Field[] = JSON.parse(fieldsJson);

  return (
    <main className="container mt-4">
      <h1 className="mb-4">${event.name}: {title}</h1>
      <p>{description}</p>
      <SchemaForm fields={fields} layout={"horizontal"} />
    </main>
  );
}
