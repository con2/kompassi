import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { getTranslations } from "@/translations";

const query = graphql(`
  query NewProgramFormSelectionQuery($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      name
      slug

      program {
        skipOfferFormSelection

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
  }
`);

interface NewProgramFormSelectionProps {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export const revalidate = 5;

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
    title: `${event?.name}: ${translations.NewProgramView.title} – Kompassi`,
  };
}

export default async function NewProgramFormSelectionPage({
  params,
}: NewProgramFormSelectionProps) {
  const { locale, eventSlug } = params;
  const t = getTranslations(locale).NewProgramView;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });
  const { event } = data;

  if (!event) {
    notFound();
  }

  const skipOfferFormSelection =
    event?.program?.skipOfferFormSelection ?? false;
  const offerForms = event.program?.offerForms ?? [];

  if (skipOfferFormSelection) {
    return redirect(`/${event.slug}/programs/new/${offerForms[0].slug}`);
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
                href={`/${event.slug}/programs/new/${offerForm.slug}`}
                aria-label={t.selectThisProgramType}
              />
            </p>
          </div>
        </div>
      ))}
    </main>
  );
}
