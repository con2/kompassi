import { notFound } from "next/navigation";
import Link from "next/link";

import { SchemaForm } from "@/components/SchemaForm";
import { Field } from "@/components/SchemaForm/models";
import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { submit } from "./actions";

const query = gql(`
  query NewProgramQuery($eventSlug:String!, $formSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name
      skipOfferFormSelection

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
  const { offerForm, skipOfferFormSelection } = event;
  if (!offerForm) {
    notFound();
  }
  const { form } = offerForm;
  const { title, description, fields: fieldsJson } = form!;
  const fields: Field[] = JSON.parse(fieldsJson);

  return (
    <main className="container mt-4">
      {skipOfferFormSelection || (
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
      <form action={submit.bind(null, locale, eventSlug, formSlug)}>
        <SchemaForm fields={fields} layout={"horizontal"} />
        <div className="row">
          <div className="col-md-3"></div>
          <div className="col-md-9">
           <button type="submit" className="btn btn-primary">{t.submit}</button>
          </div>
        </div>
      </form>
    </main>
  );
}
