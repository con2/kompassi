import Link from "next/link";
import { notFound } from "next/navigation";

import { getTranslations } from "@/translations";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { Column, DataTable } from "@/components/DataTable";
import { EventSurveyFragment } from "@/__generated__/graphql";
import { SignInRequired } from "@/components/SignInRequired";

import { auth } from "@/auth";

// this fragment is just to give a name to the type so that we can import it from generated
gql(`
  fragment EventSurvey on EventSurveyType {
    slug
    title(lang: $locale)
    isActive
    activeFrom
    activeUntil

    languages {
      language
    }
  }
`);

const query = gql(`
  query EventSurveys($eventSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        surveys {
          ...EventSurvey
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.EventSurvey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.forms?.surveys) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${t.listTitle} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function EventSurveysPage({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired translations={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.forms?.surveys) {
    notFound();
  }

  const t = translations.EventSurvey;
  const columns: Column<EventSurveyFragment>[] = [
    {
      slug: "title",
      title: t.attributes.title,
    },
    {
      slug: "isActive",
      title: t.attributes.isActive.title,
      getCell: (survey) => {
        let activityEmoji = survey.isActive ? "✅" : "❌";
        let message = "";

        if (survey.isActive) {
          if (survey.activeUntil) {
            message = t.attributes.isActive.untilTime(
              new Date(survey.activeUntil)
            );
          } else {
            message = t.attributes.isActive.untilFurtherNotice;
          }
        } else {
          if (survey.activeFrom) {
            activityEmoji = "⏳";
            message = t.attributes.isActive.openingAt(
              new Date(survey.activeFrom)
            );
          } else {
            message = t.attributes.isActive.closed;
          }
        }

        return `${activityEmoji} ${message}`;
      },
    },
    {
      slug: "languages",
      title: t.attributes.languages,
      getCell: (survey) =>
        survey.languages
          .map((language) => language.language.toLowerCase())
          .join(", "),
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCell: (survey) => (
        <>
          {survey.isActive ? (
            <Link
              href={`/events/${eventSlug}/surveys/${survey.slug}`}
              className="btn btn-sm btn-outline-primary"
            >
              {t.actions.fillIn.title}…
            </Link>
          ) : (
            <button
              disabled
              className="btn btn-sm btn-outline-primary"
              title={t.actions.fillIn.disabled}
            >
              {t.actions.fillIn.title}…
            </button>
          )}{" "}
          <Link
            href={`/events/${eventSlug}/surveys/${survey.slug}/responses`}
            className="btn btn-sm btn-outline-primary"
          >
            {t.actions.viewResponses}…
          </Link>
        </>
      ),
    },
  ];

  const surveys = data.event.forms.surveys;

  return (
    <main className="container mt-4">
      <h1>
        {t.listTitle}{" "}
        <span className="fs-5 text-muted">{t.forEvent(data.event.name)}</span>
      </h1>
      <DataTable rows={surveys} columns={columns} />
      <p>{t.tableFooter(surveys.length)}</p>
    </main>
  );
}
