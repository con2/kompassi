import { notFound, redirect } from "next/navigation";
import Link from "next/link";

import { getClient } from "@/apolloClient";
import { gql } from "@/__generated__";
import { getTranslations } from "@/translations";

const query = gql(`
  query NewProgramFormSelectionQuery($eventSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name
      slug

      offerForms {
        slug
        shortDescription(lang: $locale)
        form(lang: $locale) {
          title
          slug
        }
      }
    }
  }
`);

interface NewProgramFormSelectionProps {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export async function generateMetadata({
  params,
}: NewProgramFormSelectionProps) {
  const { locale, eventSlug } = params;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  const { event } = data;
  const translations = getTranslations(locale);
  return {
    title: `${event?.name}: ${translations.NewProgrammeView.title} – Kompassi`,
  };
}

export default async function NewProgramFormSelectionPage({
  params,
}: NewProgramFormSelectionProps) {
  const { locale, eventSlug } = params;
  const t = getTranslations(locale).NewProgrammeView;

  let data: any;
  try {
    const response = await getClient().query({
      query,
      variables: { eventSlug, locale },
    });
    data = response.data;
  } catch (err: any) {
    console.error(JSON.stringify(err.graphQLErrors, null, 2));
    throw err;
  }

  const { event } = data;

  if (!event) {
    notFound();
  }

  const offerForms = event.offerForms ?? [];

  if (offerForms.length === 1) {
    return redirect(`/events/${event.slug}/program/new/${offerForms[0].slug}`);
  }

  return (
    <main className="container mt-4">
      <h1>
        {t.title}{" "}
        <span className="fs-5 text-muted">{t.forEvent(event.name)}</span>
      </h1>
      <p>{t.engagement(event.name)}</p>

      {offerForms.map((offerForm) => (
        <div key={offerForm.slug} className="card mb-2">
          <div className="card-body">
            <h4 className="card-title">{offerForm.form?.title}</h4>
            <p className="card-text">
              {offerForm.shortDescription}
              <Link
                className="stretched-link"
                href={`/events/${event.slug}/program/new/${offerForm.slug}`}
                aria-label={t.selectThisProgramType}
              />
            </p>
          </div>
        </div>
      ))}
    </main>
  );
}
